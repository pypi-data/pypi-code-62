import glob,os
import argparse

composite_label_dict = {'ch0': 'Composite_0',
						'ch1': 'Composite_1',
						'ch2': 'Composite_2',
						'ch3': 'Composite_3',
						'ch4': 'Composite_4',
						'ch5': 'Composite_5',
						'ch6': 'Composite_6',
						'ch7': 'Composite_7',
						'ch8': 'Composite_8',
						'ch9': 'Composite_9',
						'ch10': 'Composite_10'
}

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--path', help='Path to directory with fused images for each round / channel')
	parser.add_argument('--extension', help='Image file extension',default='.tif')
	parser.add_argument('--num-channels', help='Number of channels in filename',type=int,default=3)
	parser.add_argument('--out-path', help='Path to save output')
	args,_ = parser.parse_known_args()
	Tissues = {}
	outfile = open(args.out_path,'w')
	FP = glob.glob(os.path.join(args.path,'*'+args.extension))
	for fp in sorted(FP):
		file = fp.split('/')[-1].split('.')[0]
		well = file.split('_')[0]
		round = file.split('_')[1]
		if well not in Tissues:
			Tissues[well] = 'tissue%d' % (len(Tissues) + 1)
		tissue = Tissues[well]
		channels = file.split('_')[2:2+args.num_channels]
		channel_num = int(file.split('_')[-1])-1
		if channel_num > -1:
			channel = channels[channel_num]
			if channel in composite_label_dict:
				channel = composite_label_dict[channel]
		else:
			channel = 'DAPI'
		_=outfile.write(' '.join([fp,tissue,round,channel]) + '\n')
	outfile.close()
		
		