from LinearModelFit.cache import oeid_index_to_csid_dict, csid_oeid_dict, oeid_csid_to_index_dict

import h5py
import numpy as np
from utilities import convolve

event_detection_cache_location = '/data/mat/nicholasc/LinearModelFit/LinearModelFit/cache/data/event_detection_new.h5'

def fit_receptive_field(csid, number_of_shuffles=2000, response_detection_error_std_dev=.1, seed=1):

    # Load design matrix and event vector
    f = h5py.File(event_detection_cache_location, 'r')
    A = f['A'].value.astype(float)
    b = f[str(csid)].value
    f.close()

    # Initializations:
    number_of_events = b.sum()
    np.random.seed(seed)

    # Apply gaussian blur to each frame:
    for fi in range(A.shape[1]):
        A[:16*28,fi] = convolve(A[:16 * 28, fi].reshape(16, 28)).flatten()
        A[16*28:,fi] = convolve(A[16 * 28:, fi].reshape(16, 28)).flatten()


    A = np.load('/data/mat/nicholasc/LinearModelFit/IterativeReceptiveField/A_blur.npy')
    A[np.isnan(A)] = 0

    # Create shuffled data:
    shuffle_data = np.zeros((2*16*28, number_of_shuffles))
    for ii in range(number_of_shuffles):

        size = number_of_events + int(np.round(response_detection_error_std_dev*number_of_events*np.random.randn()))
        shuffled_event_inds = np.random.choice(range(8880), size=size, replace=False)
        b_tmp = np.zeros_like(b)
        b_tmp[shuffled_event_inds] = 1
        shuffle_data[:, ii] = A.dot(b_tmp)

    # print shuffle_data.shape
    response_triggered_stimulus_vector = A.dot(b)
    p_value_list = []
    for pi in range(2*16*28):
        curr_p_value = 1-(shuffle_data[pi, :] < response_triggered_stimulus_vector[pi]).sum()*1./number_of_shuffles
        p_value_list.append(curr_p_value)

    return np.array(p_value_list)


if __name__ == "__main__":

    from utilities import plot_fields
    from statsmodels.sandbox.stats.multicomp import multipletests

    csid = 540988186
    p_values = fit_receptive_field(csid)

    alpha = .05
    p_values = np.array(multipletests(p_values, alpha=alpha))[1]
    p_values[alpha < p_values] = 1
    plot_fields(p_values)


