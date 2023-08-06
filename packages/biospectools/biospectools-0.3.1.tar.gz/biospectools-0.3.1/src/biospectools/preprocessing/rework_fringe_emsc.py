from typing import Optional
import logging

import numpy as np
import scipy
from scipy.signal import windows

from biospectools.preprocessing import emsc


# Some questions maybe answered by thinking about EMSC, FringeEMSC and ME-EMSC
# 1) Flip wavenumbers? Reference spectrum and rawspectra must have same order
# 1!) Raise warning check pearson for mean of dataset
# 2!) what if reference and preprocessing are different wavenumbers?
# 2!)Use only one wavenumbers without interpolation
# 2!) Should we keep emsc model? -> Time to create Emsc class
# 3) Use padding in fft? Need more check
# Fresnel equations: pass wavenumbers cm^-1?
# physics: wavelengths in micrometers?


class FringeEMSC:
    def __init__(
            self,
            reference: np.ndarray,
            wavenumbers: np.ndarray,
            wn_lower: float,
            wn_upper: float,
            n_freq: int,
            scaling: bool = True,
            emsc_weights: Optional[np.ndarray] = None,
            poly_order: int = 2,
            pad_length_multiplier: float = 5,
            double_freq: bool = False,
            window_function=windows.bartlett
    ):
        self.reference = reference
        self.wavenumbers = wavenumbers
        self.wn_lower = wn_lower
        self.wn_upper = wn_upper
        self.n_freq = n_freq
        self.scaling = scaling
        self.emsc_weights = emsc_weights  # Do we need to interpolate weights?
        self.poly_order = poly_order
        self.pad_length_multiplier = pad_length_multiplier
        self.double_freq = double_freq
        self.window_function = window_function

        # support invariant that wns inside always decrease
        # decreasing = self.wavenumbers[0] > self.wavenumbers[1]
        # if not decreasing:
        #     self.reference = self.reference[::-1]
        #     self.wavenumbers = self.wavenumbers[::-1]
        #     if self.emsc_weights:
        #         self.emsc_weights = self.emsc_weights[::-1]

    def transform(self, spectra):
        # maintain physical order of wavenumbers
        # decreasing = wavenumbers[0] > wavenumbers[1]
        # if not decreasing:
        #     wavenumbers = wavenumbers[::-1]
        #     spectra = spectra[:, ::-1]

        # FIXME need to give output form all iterations
        newspectra, parameters, residuals, freq_list = \
            self.correct_spectra(spectra, self.wavenumbers)

        # restore user's order
        # if not decreasing:
        #     newspectra = newspectra[:, ::-1]
        #     residuals = residuals[:, ::-1]

        return newspectra, parameters, residuals, freq_list

    def correct_spectra(self, rawspectra, wns):
        nbad = 1 + self.poly_order + 2 * self.n_freq
        if self.double_freq:
            nbad += 2 * self.n_freq
        all_corrected = []
        all_residuals = []
        all_parameters = []
        all_freqs = []
        for spec in rawspectra:
            freqs = self.frequency_from_spectrum(spec, wns)
            constituents = np.stack([sin_then_cos(freq * wns)
                                     for freq in freqs
                                     for sin_then_cos in [np.sin, np.cos]])
            corr, par, res = emsc(
                spec[None], wns, self.poly_order,
                self.reference, self.emsc_weights,
                constituents, return_coefs=True, return_residuals=True)
            all_corrected.append(corr[0])
            all_residuals.append(res[0])
            all_parameters.append(par[0])
            all_freqs.append(freqs)
        return (
            np.stack(all_corrected), np.stack(all_parameters),
            np.stack(all_residuals), np.stack(all_freqs)
        )

    # def frequencies_from_spectra(self, raw_spectra: np.ndarray, wavenumbers):
    #     assert raw_spectra.ndim == 2
    #     region = self._select_fringe_region(raw_spectra, wavenumbers)
    #     region -= region.mean()
    #     region *= self.window_function(len(region))
    #
    #     f_transform, freqs = self._apply_fft(region, wavenumbers)
    #
    #     freq_idxs, _ = scipy.signal.find_peaks(f_transform)
    #
    #     # use only N highest frequencies
    #     max_idxs = f_transform[freq_idxs].argsort()[-self.n_freq:]
    #     freq_idxs = freq_idxs[max_idxs]
    #
    #     if self.double_freq:
    #         doubled = []
    #         for freq_idx in freq_idxs:
    #             upper = f_transform[freq_idx + 1]
    #             lower = f_transform[freq_idx - 1]
    #             if upper > lower:
    #                 doubled.append(freq_idx + 1)
    #             else:
    #                 doubled.append(freq_idx - 1)
    #             doubled.append(freq_idx)
    #
    #     freq_max = freqs[np.flip(freq_idxs)]
    #     return freq_max

    def frequency_from_spectrum(self, raw_spectrum, wavenumbers):
        region = self._select_fringe_region(raw_spectrum, wavenumbers)
        region -= region.mean()
        region *= self.window_function(len(region))

        f_transform, freqs = self._apply_fft(region, wavenumbers)

        freq_idxs, _ = scipy.signal.find_peaks(f_transform)

        # use only N highest frequencies
        max_idxs = f_transform[freq_idxs].argsort()[-self.n_freq:]
        freq_idxs = freq_idxs[max_idxs]

        if self.double_freq:
            doubled = []
            for freq_idx in freq_idxs:
                upper = f_transform[freq_idx + 1]
                lower = f_transform[freq_idx - 1]
                if upper > lower:
                    doubled.append(freq_idx + 1)
                else:
                    doubled.append(freq_idx - 1)
                doubled.append(freq_idx)

        freq_max = freqs[np.flip(freq_idxs)]
        return freq_max

    @property
    def wavenumbers(self):
        return self._wavenumbers

    @wavenumbers.setter
    def wavenumbers(self, value):
        self._wavenumbers = value
        pass

    def _apply_fft(self, region, wavenumbers):
        N = self._pad_region(region)
        # N = len(padded_region)
        dw = np.abs(np.diff(wavenumbers).mean())
        freqs = 2 * np.pi * scipy.fft.fftfreq(N, dw)[0:N // 2]
        # f_transform = scipy.fft.fft(padded_region)[0:N // 2]
        f_transform = scipy.fft.fft(region, N)[0:N // 2]
        f_transform = np.abs(f_transform)
        print(f_transform)
        return f_transform, freqs

    def _pad_region(self, region):
        pad = int(len(region) * self.pad_length_multiplier)
        length = len(region) + pad
        if length % 2 == 1:
            length += 1
        return length
        # # Make sure that padded region will have odd number of points
        # if len(region) % 2 == 0:
        #     pad = (pad, pad + 1)
        # padded_region = np.pad(region, pad)
        # # padded_region it should be even
        # return padded_region

    def _select_fringe_region(self, spectra, wavenumbers):
        """
        Assumes that spectra lies along last axis
        """
        idx_lower = np.argmin(abs(wavenumbers - self.wn_lower))
        idx_upper = np.argmin(abs(wavenumbers - self.wn_upper))
        if idx_lower > idx_upper:
            idx_lower, idx_upper = idx_upper, idx_lower
        region = spectra[..., idx_lower: idx_upper].copy()
        return region


def main():
    from biospectools.physics import peak_shapes
    from biospectools.physics import misc
    from biospectools.physics import fresnel_equations
    import matplotlib.pyplot as plt

    wn = np.linspace(1000, 2500, 1500)
    wl = misc.to_wavelength(wn)

    lorentz_peak = peak_shapes.lorentzian(wn, 1600, 0.05, 5)
    nkk = misc.get_nkk(lorentz_peak, wl)
    n0 = 1.3

    n = n0 + nkk + 1j*lorentz_peak

    l = 15e-6

    t = fresnel_equations.transmission_amp(n, wl * 1e-6, l)
    T = np.abs(t)**2


    fringe_spectrum = -np.log10(T)

    # wn = wn/100
    fringeEMSCmodelEMSC = FringeEMSC(
        reference=lorentz_peak*10,
        wavenumbers=wn,
        wn_lower=1800, wn_upper=2320,
        n_freq=2, scaling=True, poly_order=1,
        pad_length_multiplier=2.5, double_freq=True)

    lol = np.vstack((fringe_spectrum, fringe_spectrum))
    corr, par, res, freqList = fringeEMSCmodelEMSC.transform(lol)

    plt.figure()
    plt.plot(wn, fringe_spectrum)
    plt.plot(wn, corr[0])
    plt.show()

    # fringeEMSCmodelEMSC2 = FringeEMSC2(refSpec=lorentz_peak*10, wnref=wn, wnLower=1800, wnUpper=2320, nFreq=1,
    #                                    scaling=True, polyorder=1, Npad=2.5, double_freq=True)

    # corr, par, res, freqList = fringeEMSCmodelEMSC2.transform(fringe_spectrum[np.newaxis, :], wn)
    #
    # plt.figure()
    # plt.plot(wn, fringe_spectrum)
    # plt.plot(wn, corr[0,:])
    # plt.show()

    print('lol')

if __name__ == '__main__':
    main()


#
#
# if __name__ == '__main__':
#     from biospectools.physics import peak_shapes
#     from biospectools.physics import misc
#     from biospectools.physics import fresnel_equations
#     import matplotlib.pyplot as plt
#
#     wn = np.linspace(1000, 2500, 1500)
#     wl = misc.to_wavelength(wn)
#
#     lorentz_peak = peak_shapes.lorentzian(wn, 1600, 0.05, 5)
#     nkk = misc.get_nkk(lorentz_peak, wl)
#     n0 = 1.3
#
#     n = n0 + nkk + 1j*lorentz_peak
#
#     l = 15e-6
#
#     t = fresnel_equations.transmission_amp(n, wl * 1e-6, l)
#     T = np.abs(t)**2
#
#
#     fringe_spectrum = -np.log10(T)
#
#     # wn = wn/100
#     fringeEMSCmodelEMSC = FringeEMSC(
#         reference=lorentz_peak * 10,
#         wavenumbers=wn,
#         fringe_location=(1800, 2320),
#         n_freq=2, scale=True, poly_order=1,
#         pad_length_multiplier=2.5, double_freq=False)
#     # fringeEMSCmodelEMSC = FringeEMSC(refSpec=lorentz_peak*10, wnref=wn, wnLower=1800, wnUpper=2320, nFreq=2,
#     #                                  scaling=True, polyorder=1, Npad=2.5, double_freq=True)
#
#     lol = np.vstack((fringe_spectrum, fringe_spectrum))
#     corr = fringeEMSCmodelEMSC.transform(lol)
#
#     plt.figure()
#     plt.plot(wn, fringe_spectrum)
#     plt.plot(wn, corr[0])
#     plt.show()
#
#     print('lol')
