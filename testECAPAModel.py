'''
This is the main code of the ECAPATDNN project, to define the parameters and build the construction
'''

import argparse, glob, os, torch, warnings, time
from tools import *
from dataLoader import train_loader
from ECAPAModel import ECAPAModel


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "ECAPA_trainer")
	## Training Settings
	parser.add_argument('--num_frames', type=int,   default=200,     help='Duration of the input segments, eg: 200 for 2 second')
	parser.add_argument('--max_epoch',  type=int,   default=80,      help='Maximum number of epochs')
	parser.add_argument('--batch_size', type=int,   default=128,     help='Batch size')
	parser.add_argument('--n_cpu',      type=int,   default=4,       help='Number of loader threads')
	parser.add_argument('--test_step',  type=int,   default=1,       help='Test and save every [test_step] epochs')
	parser.add_argument('--lr',         type=float, default=0.001,   help='Learning rate')
	parser.add_argument("--lr_decay",   type=float, default=0.98,    help='Learning rate decay every [test_step] epochs')

	## Training and evaluation path/lists, save path
	parser.add_argument('--train_list', type=str,   default="/data08/VoxCeleb2/train_list.txt",     help='The path of the training list, https://www.robots.ox.ac.uk/~vgg/data/voxceleb/meta/train_list.txt')
	parser.add_argument('--train_path', type=str,   default="../../voxceleb1_full_dataset/wav_train",        help='The path of the training data, eg:"/data08/VoxCeleb2/train/wav" in my case')
	
 
	parser.add_argument('--eval_list',  type=str,   default="../../voxceleb1_full_dataset/veri_test2.txt",   help='The path of the evaluation list, veri_test2.txt comes from https://www.robots.ox.ac.uk/~vgg/data/voxceleb/meta/veri_test2.txt')
	parser.add_argument('--eval_path',  type=str,   default="../../voxceleb1_full_dataset/wav_test",         help='The path of the evaluation data, eg:"/data08/VoxCeleb1/test/wav" in my case')
	
	#parser.add_argument('--eval_list',  type=str,   default="../../voxceleb_dataset/voxceleb2_dev_iip/voxceleb2_dev_iip/voxceleb2_dev_iip.txt",   help='The path of the evaluation list, veri_test2.txt comes from https://www.robots.ox.ac.uk/~vgg/data/voxceleb/meta/veri_test2.txt')
	#parser.add_argument('--eval_path',  type=str,   default="../../voxceleb_dataset/voxceleb2_dev_iip/voxceleb2_dev_iip/",         help='The path of the evaluation data, eg:"/data08/VoxCeleb1/test/wav" in my case')
	parser.add_argument('--musan_path', type=str,   default="../../musan/",                    help='The path to the MUSAN set, eg:"/data08/Others/musan_split" in my case')
	parser.add_argument('--rir_path',   type=str,   default="../../rirs_noises/RIRS_NOISES/simulated_rirs",     help='The path to the RIR set, eg:"/data08/Others/RIRS_NOISES/simulated_rirs" in my case');
	parser.add_argument('--save_path',  type=str,   default="exps/exp1",                                     help='Path to save the score.txt and models')
	parser.add_argument('--initial_model',  type=str,   default="exps/exp1/model/model_0062.model",                                          help='Path of the initial_model')

	## Model and Loss settings
	parser.add_argument('--C',       type=int,   default=1024,   help='Channel size for the speaker encoder')
	parser.add_argument('--m',       type=float, default=0.2,    help='Loss margin in AAM softmax')
	parser.add_argument('--s',       type=float, default=30,     help='Loss scale in AAM softmax')
	parser.add_argument('--n_class', type=int,   default=1211,   help='Number of speakers')

	## Command
	parser.add_argument('--eval',    dest='eval', default=True, action='store_true', help='Only do evaluation')

	## Initialization
	warnings.simplefilter("ignore")
	torch.multiprocessing.set_sharing_strategy('file_system')
	args = parser.parse_args()
	args = init_args(args)


	## Only do evaluation, the initial_model is necessary
	if args.eval == True:
		s = ECAPAModel(**vars(args))
		print("Model %s loaded from previous state!"%args.initial_model)

		s.load_parameters(args.initial_model)
		EER, minDCF = s.eval_network(eval_list = args.eval_list, eval_path = args.eval_path)
		print("EER %2.2f%%, minDCF %.4f%%"%(EER, minDCF))
		quit()
