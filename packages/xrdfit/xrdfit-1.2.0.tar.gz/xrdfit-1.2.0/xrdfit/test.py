import yaml

from xrdfit.spectrum_fitting import PeakParams, FitSpectrum, peak_params_from_dict

with open("../tutorial notebooks/example_input.yaml") as input_file:
    data = yaml.safe_load(input_file)

peak_params = peak_params_from_dict(data["peak_params"])


first_cake_angle = 90
file_path = '../example_data/adc_041_7Nb_NDload_700C_15mms_00001.dat'
spectral_data = FitSpectrum(file_path, first_cake_angle)

peak_params = PeakParams((2.75, 2.95), '(10-10)')
spectral_data.fit_peaks(peak_params, 1)
spectral_data.plot_fit('(10-10)')
