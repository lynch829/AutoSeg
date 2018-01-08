from AutoSeg.Learner.learner import *
import os
import pickle

from AutoSeg.Dicom.image_constants import *
import imp

#learner = Unet25('','','','','','','','')
FLAGS_train             = 0
FLAGS_train_data_dir    = 'aapm_journal_localtest/Small/Hdf5/test'
FLAGS_test_data_dir     = 'aapm_journal_localtest/Small/Hdf5/test'
FLAGS_checkpoint_dir    = 'checkpoint'
FLAGS_log_dir           = 'logs'

def main():

    #setup training, testing list
    if FLAGS_train_data_dir == FLAGS_test_data_dir: #training with 2/3 slit
        testing_gt_available = True
        a = a*2
        if os.path.exists( os.path.join( FLAGS_train_data_dir, 'files.log')):
            with open( os.path.join( FLAGS_train_data_dir, 'files.log'), 'r') as f:
                training_paths, testing_paths = pickle.load(f)
        else:
            all_subjects    = [ os.path.join( FLAGS_train_data_dir, name) for name in os.listdir( FLAGS_train_data_dir)]
            n_training      = int( len(all_subjects) * 2 /3)
            training_paths  = all_subjects[:n_training]
            testing_paths   = all_subjects[n_training:]
            with open( os.path.join( FLAGS_train_data_dir, 'files.log'), 'w') as f:
                pickle.dump( [training_paths, testing_paths], f)

    else: #train and test together, not recommend
        raise ValueError ('Not recommend for prototype because train and test together is waste of time')

    if not os.path.exists( FLAGS_checkpoint_dir):
        os.makedirs(FLAGS_checkpoint_dir)

    if not os.path.exists( FLAGS_log_dir):
        os.makedirs( FLAGS_log_dir)

    model = imp.load_source('model', 'AutoSeg/Models/Unet25_model.py')
    model_func = model.get_unet

    learner_all = Unet25(checkpoint_dir= FLAGS_checkpoint_dir, log_dir = FLAGS_log_dir,
                         training_paths=training_paths, testing_paths = testing_paths,
                         roi = (-1, 'All'), im_size=RE_SIZE,
                         model_func=model_func,
                         train_model_name=None, test_model_name=None,
                         nclass=N_CLASSES + 1 )

    if FLAGS_train:
        learner_all.train()
    else:
        learner_all.test()

    print ('Result is good')

if __name__ == '__main__':
    main()