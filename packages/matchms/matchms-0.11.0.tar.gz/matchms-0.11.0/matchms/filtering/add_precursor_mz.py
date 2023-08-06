import logging
from matchms.utils import get_first_common_element
from ..typing import SpectrumType


logger = logging.getLogger("matchms")


_accepted_keys = ["precursor_mz", "precursormz", "precursor_mass"]
_accepted_types = (float, str, int)


def add_precursor_mz(spectrum_in: SpectrumType) -> SpectrumType:
    """Add precursor_mz to correct field and make it a float.

    For missing precursor_mz field: check if there is "pepmass"" entry instead.
    For string parsed as precursor_mz: convert to float.
    """
    if spectrum_in is None:
        return None

    spectrum = spectrum_in.clone()

    precursor_mz_key = get_first_common_element(spectrum.metadata.keys(), _accepted_keys)
    precursor_mz = spectrum.get(precursor_mz_key)

    if isinstance(precursor_mz, _accepted_types):
        if isinstance(precursor_mz, str):
            try:
                precursor_mz = float(precursor_mz.strip())
            except ValueError:
                logger.warning("%s can't be converted to float.", precursor_mz)
                return spectrum
        spectrum.set("precursor_mz", float(precursor_mz))
    elif precursor_mz is None:
        pepmass = spectrum.get("pepmass")
        if pepmass is not None and isinstance(pepmass[0], float):
            spectrum.set("precursor_mz", pepmass[0])
        else:
            logger.warning("No precursor_mz found in metadata.")

    return spectrum
