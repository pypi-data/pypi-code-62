import tensorflow as tf
import numpy as np

#from tensorflow.keras import Input
#from tensorflow.keras.models import Model
#from tensorflow.keras.layers import Layer,Embedding

#from xlnet_layers import EmbeddingRet,EmbeddingSim

#from xlnet_configuration import XLNetConfig 
from .xlnet_configuration import XLNetConfig

if tf.config.experimental.list_physical_devices('GPU'):
    from toolsbyerazhan.gputools import set_gpu_memory_tf
    set_gpu_memory_tf()

def gelu(x):
    return 0.5 * x * (1.0 + tf.math.erf(x / np.sqrt(2.0)))
'''
#后续依次加上
custom_objects = {
    'gelu':gelu
    }
#也可以直接用赋值的方式
tf.keras.utils.get_custom_objects().update(custom_objects)

#最好都是把pad设置为0,可以 省去很多麻烦
#build_xlnet中mask_index!=0的情况暂时不考虑？
#这个不记得在哪里用了
'''
#{XLNetConfig,}注释掉的是原版

'''
#测试自定义的XLNetConfig
#config_class = XLNetConfig()
#print(config_class.vocab_size)
'''

class TFXLNetMainLayer(tf.keras.layers.Layer):
    '''config参数在其它地方赋值'''
    def __init__(self,config,**kwargs):
        super().__init__(**kwargs)
        self.output_hidden_states = config.output_hidden_states
        self.oupput_attentions = config.output_attentions
        self.return_dict = config.return_dict#这是个啥

        self.mem_len = config.mem_len
        self.reuse_len = config.reuse_len
        self.d_model = config.d_model
        self.same_length = config.same_length#保留吧,在create_uni_mask中使用到
        self.attn_type = config.attn_type
        self.bi_data = config.bi_data#不考虑
        self.clamp_len = config.clamp_len
        self.n_layer = config.n_layer
        #self.use_bfloat16 = config.use_bfloat16#统统用tf.float32
        self.initializer_range = config.initializer_range

        self.word_embedding = TFSharedEmbeddings(
            config.vocab_size, config.d_model, initializer_range=config.initializer_range, name="word_embedding"
        )
        self.layer = [TFXLNetLayer(config, name="layer_._{}".format(i)) for i in range(config.n_layer)]
        self.dropout = tf.keras.layers.Dropout(config.dropout)

    def build(self,input_shape):

        initializer = get_initializer(self.initializer_range)
        #在modeling_tf_utils中定义

        #这个用于构造初始query stream中的g,对应[num_predict,bsz,d_model],表示要预测token的词向量表示
        self.mask_emb = self.add_weight(shape = (1,1,self.d_model),initializer = initializer, trainable = True, name = "mask_emb")

    def create_uni_mask(self,qlen, mlen, dtype = tf.float32):
        '''单向模型时产生初始的attn_mask,此时不需要双向模型的perm_mask'''
        
        """
        Creates causal attention mask. Float mask where 1.0 indicates masked, 0.0 indicates not-masked.

        Args:
            qlen: TODO Lysandre didn't fill
            mlen: TODO Lysandre didn't fill

        ::

                  same_length=False:      same_length=True:
                  <mlen > <  qlen >       <mlen > <  qlen >
               ^ [0 0 0 0 0 1 1 1 1]     [0 0 0 0 0 1 1 1 1]
                 [0 0 0 0 0 0 1 1 1]     [1 0 0 0 0 0 1 1 1]
            qlen [0 0 0 0 0 0 0 1 1]     [1 1 0 0 0 0 0 1 1]
                 [0 0 0 0 0 0 0 0 1]     [1 1 1 0 0 0 0 0 1]
               v [0 0 0 0 0 0 0 0 0]     [1 1 1 1 0 0 0 0 0]

        """
        attn_mask = tf.ones([qlen, qlen], dtype=dtype)
        mask_u = tf.linalg.band_part(attn_mask, 0, -1)
        mask_dia = tf.linalg.band_part(attn_mask, 0, 0)
        attn_mask_pad = tf.zeros([qlen, mlen], dtype=dtype)
        ret = tf.concat([attn_mask_pad, mask_u - mask_dia], 1)
        if self.same_length:
            mask_l = tf.linalg.band_part(attn_mask, -1, 0)
            ret = tf.concat([ret[:, :qlen] + mask_l - mask_dia, ret[:, qlen:]], 1)
        return ret

    def cache_mem(self,curr_out,prev_mem):
        #关于mem的用法还不是很懂
        pass

    @staticmethod
    def positional_embedding(pos_seq, inv_freq, bsz=None):
        sinusoid_inp = tf.einsum("i,d->id", pos_seq, inv_freq)
        pos_emb = tf.concat([tf.sin(sinusoid_inp), tf.cos(sinusoid_inp)], axis=-1)
        pos_emb = pos_emb[:, None, :]

        if bsz is not None:
            pos_emb = tf.tile(pos_emb, [1, bsz, 1])

        return pos_emb

    def relative_positional_encoding(self, qlen, klen, bsz=None, dtype = tf.float32):
        """create relative positional encoding."""
        freq_seq = tf.range(0, self.d_model, 2.0)
        freq_seq = tf.cast(freq_seq, dtype=dtype)

        inv_freq = 1 / (10000 ** (freq_seq / self.d_model))
        assert self.att_type == "bi" or self.att_type == "uni", "att_type must be 'bi' or 'uni'"
        if self.attn_type == "bi":
            # beg, end = klen - 1, -qlen
            beg, end = klen, -qlen
        else:#self.attn_type == "uni"
            # beg, end = klen - 1, -1
            beg, end = klen, -1

        fwd_pos_seq = tf.range(beg, end, -1.0)
        fwd_pos_seq = tf.cast(fwd_pos_seq, dtype = dtype)
        if self.clamp_len > 0:
            fwd_pos_seq = tf.clip_by_value(fwd_pos_seq, -self.clamp_len, self.clamp_len)
        pos_emb = self.positional_embedding(fwd_pos_seq, inv_freq, bsz)#bsz仅仅用处只有一个

        return pos_emb

    def call(self,
             inputs,
             attention_mask = None,
             mems = None,
             perm_mask = None,
             target_mapping = None,
             token_type_ids = None,
             input_mask = None,
             #head_mask = None,#这个暂不考虑
             inputs_embeds = None,
             use_cache = True,
             output_attentions = None,
             output_hidden_states = None,
             #return_dict = None,#这个是新版本的,不考虑
             training = False
             ):
        #判断inputs格式,至少有input_ids,这里暂不考虑dict,BatchEncoding格式(源码中的第2种)
        if isinstance(inputs, (tuple,list)):
            #输入严格按照顺序来
            input_ids = inputs[0]#[bsz,qlen]
            attention_mask = inputs[1] if len(inputs) > 1 else attention_mask#[bsz,qlen,qlen],0代表mask
            mems = inputs[2] if len(inputs) > 2 else mems#列表,个数是attention的层数,后续补充使用说明
            perm_mask = inputs[3] if len(inputs) > 3 else perm_mask#[bsz,qlen,qlen(klen?)]
            target_mapping = inputs[4] if len(inputs) > 4 else target_mapping#维度[bsz,num_predict,qlen(klen)]
            token_type_ids = inputs[5] if len(inputs) > 5 else token_type_ids#[bsz,qlen]
            input_mask = inputs[6] if len(inputs) > 6 else input_mask#[bsz,qlen],和attention_mask相反,1代表mask
            #head_mask = inputs[7] if len(inputs) > 7 else head_mask#对不同的head进行mask,暂不考虑
            inputs_embeds = inputs[8] if len(inputs) > 8 else inputs_embeds#[bsz,qlen,d_model(hidden_size)]就是word_embedding(input_ids)
            use_cache = inputs[9] if len(inputs) > 9 else use_cache#是否使用memory机制,默认True
            output_attentions = inputs[10] if len(inputs) > 10 else output_attentions#是否输出每个attention层后的qk(还没到qkv),暂不考虑
            output_hidden_states = inputs[11] if len(inputs) > 11 else output_hidden_states##输出每一层的结果(后续再完善理解),暂不考虑
            assert len(inputs) <= 12, "Too many inputs."
        else:
            input_ids = inputs

        #放这里,先不考虑
        #output_attentions = output_attentions if output_attentions is not None else self.output_attentions
        #output_hidden_states = output_hidden_states if output_hidden_states is not None else self.output_hidden_states
        
        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both input_ids and inputs_embeds at the same time")
        elif input_ids is not None:#[bsz,qlen]->[qlen,bsz]
            input_ids = tf.transpose(input_ids, perm=(1, 0))
            qlen, bsz = shape_list(input_ids)[:2]
        elif inputs_embeds is not None:#[bsz,qlen,d_model]->[qlen,bsz,d_model]
            inputs_embeds = tf.transpose(inputs_embeds, perm=(1, 0, 2))
            qlen, bsz = shape_list(inputs_embeds)[:2]
        else:
            raise ValueError("You have to specify either input_ids or inputs_embeds")

        token_type_ids = tf.transpose(token_type_ids, perm=(1, 0)) if token_type_ids is not None else None#[bsz,qlen]->[qlen,bsz]
        input_mask = tf.transpose(input_mask, perm=(1, 0)) if input_mask is not None else None#[bsz,qlen]->[qlen,bsz]
        attention_mask = tf.transpose(attention_mask, perm=(1, 0)) if attention_mask is not None else None#[bsz,qlen]->[qlen,bsz]
        perm_mask = tf.transpose(perm_mask, perm=(1, 2, 0)) if perm_mask is not None else None#[bsz,qlen,klen]->[qlen,klen,bsz]
        target_mapping = tf.transpose(target_mapping, perm=(1, 2, 0)) if target_mapping is not None else None#[bsz,num_predict,qlen]->[num_predict,qlen,bsz]

        mlen = shape_list(mems[0])[0] if mems is not None and mems[0] is not None else 0#mlen和memory有关
        klen = mlen + qlen

        # Attention mask
        # causal attention mask
        if self.attn_type == "uni":#选择单向模型,此处得到的atten_mask其实和Transformer的decoder的mask一样，注意该符号和attention_mask的区别
            attn_mask = self.create_uni_mask(qlen, mlen)
            attn_mask = attn_mask[:, :, None, None]#[qlen,klen]->[qlen,klen,1(bsz),1(d_model)]
        elif self.attn_type == "bi":#选择双向模型,此时不用attn_mask,而是用perm_mask,二者只需一个
            attn_mask = None
        else:
            raise ValueError("Unsupported attention type: {}".format(self.attn_type))

















        
