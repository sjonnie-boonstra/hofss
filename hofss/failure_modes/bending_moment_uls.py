from abc import ABCMeta, abstractmethod  # Abstract Base Class (ABC)

from ..data_structures import Parameter


def bendingMomentULS(
    theta_R: float, A_s: float, f_yd: float, h: float, c: float, diam: float, alpha: float,
    beta: float, f_cd: float, b: float, theta_E: float, p_d: float, p_G: float, L: float, *args, **kwargs
):
    """determines the failure criterion Z Capacity - Acting force for this fialure mode if Z < 0, failure occurs.

    Args:
        theta_R (float): uncertainty factor of resistance
        A_s (float): surface area of reinforcement [mm2]
        f_yd (float): design value of the reinforcement's yield strength [N/mm2]
        h (float): height of the slab [mm]
        c (float): concrete cover [mm]
        diam (float): _description_
        alpha (float): concrete zone shape factor [-]
        beta (float): concrete zone shape factor [-]
        f_cd (float): design value of the concrete's compressive strength [N/mm2]
        b (float): slab width [mm]
        theta_E (float): uncertainty factor of load effect [-]
        p_d (float): design load [N/mm2]
        p_G (float): self weight [N/mm2]
        L (float): span length [mm]

    Returns:
        float: the failure criterion
    """
    capacity = theta_R * A_s * f_yd * (h - c - diam/2 - ((alpha * A_s * f_yd) / (beta * f_cd * b)))
    acting_force = (theta_E * (p_G + p_d) * L**2) / 8.0
    return capacity - acting_force
