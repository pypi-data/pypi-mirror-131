import os
import sys

flag = sys.argv[1]

################################################################################# for demo ######################################################################################################
# Only train, using 1 GPU and batch_size=1
if flag == 'train':
    os.system('python train.py --datasets_folder DataForPytorch --n_epochs 30 --GPU 0 --train_datasets_size 3500')  

# just test 300 slices for demo
if flag == 'test':
    os.system('python test.py --denoise_model ModelForPytorch --datasets_folder DataForPytorch --GPU 0 --batch_size 1 --test_datasize 300')

################################################################################ my experiments ##################################################################################################
# debug ##########################################################################################################################################################################################
if flag == 'train-debug': 
    os.system('python train.py --datasets_folder 23-NP3D-area2 --n_epochs 20 --GPU 0 --patch_x 150 --train_datasets_size 6000')


################################################################################ my experiments ##################################################################################################
# test data augmentation ##########################################################################################################################################################################################
if flag == 'train-aug': 
    os.system('python train.py --datasets_folder 9-test-overfitting --n_epochs 50 --GPU 1 --train_datasets_size 6000')
if flag == 'test-aug':
    os.system('python test.py --denoise_model 9-test-overfitting_aug --datasets_folder 9-test-overfitting --GPU 0 --test_datasize 300')

if flag == 'train-noaug': 
    os.system('python train.py --datasets_folder 9-test-overfitting --n_epochs 50 --GPU 0 --train_datasets_size 6000')
if flag == 'test-noaug':
    os.system('python test.py --denoise_model 9-test-overfitting_nonaug --datasets_folder 9-test-overfitting --GPU 0 --test_datasize 300')

# neutrophil 3D ##################################################################################################################################################################################
if flag == 'train-NP3D': 
    os.system('python train.py --datasets_folder 23-NP3D-area2 --n_epochs 80 --GPU 0,1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')

if flag == 'test-NP3D':
    os.system('python test.py --denoise_model 23-NP3D-area2-multistack-GM --datasets_folder 23-NP3D-area2 --GPU 0,1 --test_datasize 30000')

# ATP 3D #########################################################################################################################################################################################
if flag == 'train-ATP3D':
    os.system('python train.py --datasets_folder 32-ATP3D-15slice --n_epochs 20 --GPU 1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')

if flag == 'test-ATP3D':
    os.system('python test.py --denoise_model 32-ATP3D-multistack-GM --datasets_folder 32-ATP3D-all --GPU 0,1 --test_datasize 30000')
# different SNR ######################################################################################################################
# 3090
if flag == 'train-1':
    os.system('python train.py --datasets_folder 1RPN --n_epochs 10 --GPU 2 --patch_x 150 --overlap_factor 0.15 --train_datasets_size 6000')

if flag == 'train-largeov':
    os.system('python train.py --datasets_folder 2RPN --n_epochs 13 --GPU 1 --patch_x 150 --overlap_factor 0.5 --train_datasets_size 6000')
    os.system('python train.py --datasets_folder 4RPN --n_epochs 13 --GPU 1 --patch_x 150 --overlap_factor 0.5 --train_datasets_size 6000')
    # os.system('python train.py --datasets_folder 7RPN --n_epochs 10 --GPU 1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
if flag == 'train-2':
    os.system('python train.py --datasets_folder 20RPN --n_epochs 10 --GPU 2 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
    os.system('python train.py --datasets_folder 40RPN --n_epochs 10 --GPU 2 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')


if flag == 'train-20':
    os.system('python train.py --datasets_folder 20RPN --n_epochs 20 --GPU 0 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
if flag == 'train-40':
    os.system('python train.py --datasets_folder 40RPN --n_epochs 20 --GPU 1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')

if flag == 'test-1':

    os.system('python test-nospost-snr.py --denoise_model 1RPN_202112062022 --datasets_folder 1RPN --GPU 0,1 --test_datasize 6000 --overlap_factor 0.45')

    # os.system('python test-nospost-snr.py --denoise_model 2RPN_202112070244 --datasets_folder 2RPN --GPU 0,1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --denoise_model 4RPN_202112062025 --datasets_folder 4RPN --GPU 0,1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --denoise_model 7RPN_202112070242 --datasets_folder 7RPN --GPU 0,1 --test_datasize 6000')
    # os.system('python test.py --denoise_model 150RPN_202111280900 --datasets_folder 150RPN --GPU 0,1 --test_datasize 6000')
    # os.system('python test.py --denoise_model 75RPN_202111280859 --datasets_folder 75RPN --GPU 0,1 --test_datasize 6000')
    # os.system('python test.py --denoise_model 4RPN_202111290839 --datasets_folder 4RPN --GPU 0 --test_datasize 6000')
    # os.system('python test.py --denoise_model 375RPN_202111290836 --datasets_folder 375RPN --GPU 0 --test_datasize 6000')

if flag == 'train-1000f':
     os.system('python train.py --datasets_folder 2RPN-1000 --n_epochs 20 --GPU 0 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 5600')
    # os.system('python train.py --datasets_folder 2RPN --n_epochs 20 --GPU 0 --patch_x 150 --overlap_factor 0.25 --select_img_num 1000 --train_datasets_size 5600')
    # os.system('python train.py --datasets_folder 2RPN --n_epochs 20 --GPU 1 --patch_x 150 --overlap_factor 0.25 --select_img_num 3000 --train_datasets_size 6000')
if flag == 'train-2000f':
    os.system('python train.py --datasets_folder 2RPN-2000 --n_epochs 20 --GPU 1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
if flag == 'train-4000f':
    os.system('python train.py --datasets_folder 2RPN-4000 --n_epochs 20 --GPU 1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
    os.system('python train.py --datasets_folder 2RPN-5000 --n_epochs 20 --GPU 1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
if flag == 'train-2-long':
    os.system('python train.py --datasets_folder 2RPN-1000 --n_epochs 50 --GPU 2 --patch_x 150 --overlap_factor 0.5 --train_datasets_size 5700')


if flag == 'test-64fmap':
    os.system('python test.py --denoise_model 375RPN_202111290836 --datasets_folder 2RPN --GPU 0 --test_datasize 6000 --fmap 64')

# 3080
if flag == 'train-4':
    os.system('python train.py --datasets_folder 4RPN --n_epochs 20 --GPU 2 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
if flag == 'train-375':
    os.system('python train.py --datasets_folder 375RPN --n_epochs 20 --GPU 1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
# if flag == 'train-7':
#     os.system('python train.py --datasets_folder 7RPN --n_epochs 20 --GPU 1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
# if flag == 'train-12':
#     os.system('python train.py --datasets_folder 12RPN --n_epochs 20 --GPU 2 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')



if flag == 'train-75':
    os.system('python train.py --datasets_folder 75RPN --n_epochs 20 --GPU 1 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')
if flag == 'train-150':
    os.system('python train.py --datasets_folder 150RPN --n_epochs 20 --GPU 2 --patch_x 150 --overlap_factor 0.25 --train_datasets_size 6000')

if flag == 'test-snr':
    # os.system('python test-nospost-snr.py --denoise_model 2RPN-1000_202112021909 --datasets_folder 2RPN --GPU 1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --denoise_model 2RPN-2000_202111292134 --datasets_folder 2RPN --GPU 1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --denoise_model 2RPN-3000_202112021911 --datasets_folder 2RPN --GPU 1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --denoise_model 2RPN-4000_202112040844 --datasets_folder 2RPN --GPU 1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --denoise_model 2RPN-5000_202112050145 --datasets_folder 2RPN --GPU 1 --test_datasize 6000')


    # os.system('python test-nospost-snr.py --denoise_model 2RPN_202111262150 --datasets_folder 2RPN --GPU 0 --test_datasize 6000 --overlap_factor 0.4')
    # os.system('python test-nospost-snr.py --fmap 64  --denoise_model 2RPN_202111301445_64fmap_noaug --datasets_folder 2RPN --patch_x 150 --GPU 0,1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --fmap 48 --denoise_model 2RPN_202112051316_48fmap_noaug --datasets_folder 2RPN --GPU 0,1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --fmap 32  --denoise_model 2RPN_202111302128_32fmap_noaug --datasets_folder 2RPN --patch_x 150 --GPU 0,1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --fmap 24  --denoise_model 2RPN_202112011330_24fmap_noaug --datasets_folder 2RPN --patch_x 150 --GPU 0,1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --fmap 16  --denoise_model 2RPN_202111302139_16fmap_noaug --datasets_folder 2RPN --patch_x 150 --GPU 0,1 --test_datasize 6000')
    # os.system('python test-nospost-snr.py --denoise_model 1RPN_202112071152_lr_small --datasets_folder 1RPN --GPU 1,2 --test_datasize 600')
    os.system('python test-nospost-snr.py --denoise_model 1RPN_202112101134_ov_0.15 --datasets_folder 1RPN --GPU 2 --test_datasize 600')
