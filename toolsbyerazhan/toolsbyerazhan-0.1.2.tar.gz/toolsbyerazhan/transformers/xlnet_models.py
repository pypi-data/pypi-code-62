import tensorflow as tf
import numpy as np

from toolsbyerazhan.gputools import set_gpu_memory_tf

#{XLNetConfig,}注释掉的是原版
#from .configuration_xlnet import XLNetConfig
#from xlnet_configuration import XLNetConfig 
'''
if tf.test.is_gpu_available():
    from configure_gpu import set_gpu_memory
    set_gpu_memory()

#测试自定义的XLNetConfig
#config_class = XLNetConfig()
#print(config_class.vocab_size)

class TFXLNetMainLayer(tf.keras.layers.Layer):
    #源码中有另外的使用方式(暂时不记得了,好像是PretrainedConfig)
    #config_class = XLNetConfig
    def __init__(self, config, **kwargs):
        super(TFXLNetMainLayer).__init__(**kwargs)
        self.output_hidden_states = config.output_hidden_states
'''
__all__ = ["TFXLNetMainLayer","tfun"]

def tfun():
    if tf.config.experimental.list_physical_devices('GPU'):
        set_gpu_memory()
    print("测试set_gpu_memory能否使用")


def tfun1():
    print("这里应该用不上")
#tfun()
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
        self.same_length = config.same_length
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

    def create_uni_mask(self,qlen, mlen,dtype = tf.float32):
        '''当采用单向模型,没有perm_mask'''
        #源码和当前版本不一致
        pass

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
             return_dict = None,
             training = False
             ):
        pass


        
