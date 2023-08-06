"""This module is part of the PeptideConstructor library, written (improved) by CharlesHahn. This pacage is based on Lun4m/PeptideBuilder.git and clauswilke/PeptideBuilder.git. 

The PeptideBuilder module contains code to generate 3D structures of (DL-) peptides. It requires the Geometry module, which contains default bond lengths and angles for all amino acids.

This module also requires the Bio.PDB module from
Biopython for structure manipulation and numpy for coordinates calculation.

This file is provided to you under the MIT License."""

import math, warnings
from typing import List, Optional, Union

from Bio.PDB.Polypeptide import is_aa
from Bio.PDB.Atom import Atom
from Bio.PDB.Residue import Residue
from Bio.PDB.Chain import Chain
from Bio.PDB.Model import Model
from Bio.PDB.Structure import Structure
from Bio.PDB.vectors import Vector, rotaxis, calc_dihedral, calc_angle
import numpy as np

from .Geometry import (
    AlaGeo,
    ArgGeo,
    AsnGeo,
    AspGeo,
    CysGeo,
    GlnGeo,
    GluGeo,
    GlyGeo,
    HisGeo,
    IleGeo,
    LeuGeo,
    LysGeo,
    MetGeo,
    PheGeo,
    ProGeo,
    SerGeo,
    ThrGeo,
    TrpGeo,
    TyrGeo,
    ValGeo,
    AceGeo,
    NmeGeo,
    geometry,
    Geo,
    DGlyGeo,
    DAlaGeo,
    DArgGeo,
    DAsnGeo,
    DAspGeo,
    DCysGeo,
    DGlnGeo,
    DGluGeo,
    DHisGeo,
    DIleGeo,
    DLeuGeo,
    DLysGeo,
    DMetGeo,
    DPheGeo,
    DProGeo,
    DSerGeo,
    DThrGeo,
    DTrpGeo,
    DTyrGeo,
    DValGeo,
)


def calculateCoordinates(
    refA: Residue, refB: Residue, refC: Residue, L: float, ang: float, di: float
) -> np.ndarray:
    AV = refA.get_vector()
    BV = refB.get_vector()
    CV = refC.get_vector()

    CA = AV - CV
    CB = BV - CV

    ##CA vector
    AX = CA[0]
    AY = CA[1]
    AZ = CA[2]

    ##CB vector
    BX = CB[0]
    BY = CB[1]
    BZ = CB[2]

    ##Plane Parameters
    A = (AY * BZ) - (AZ * BY)
    B = (AZ * BX) - (AX * BZ)
    G = (AX * BY) - (AY * BX)

    ##Dot Product Constant
    F = math.sqrt(BX * BX + BY * BY + BZ * BZ) * L * math.cos(ang * (math.pi / 180.0))

    ##Constants
    const = math.sqrt(
        math.pow((B * BZ - BY * G), 2)
        * (
            -(F * F) * (A * A + B * B + G * G)
            + (
                B * B * (BX * BX + BZ * BZ)
                + A * A * (BY * BY + BZ * BZ)
                - (2 * A * BX * BZ * G)
                + (BX * BX + BY * BY) * G * G
                - (2 * B * BY) * (A * BX + BZ * G)
            )
            * L
            * L
        )
    )
    denom = (
        (B * B) * (BX * BX + BZ * BZ)
        + (A * A) * (BY * BY + BZ * BZ)
        - (2 * A * BX * BZ * G)
        + (BX * BX + BY * BY) * (G * G)
        - (2 * B * BY) * (A * BX + BZ * G)
    )

    X = (
        (B * B * BX * F) - (A * B * BY * F) + (F * G) * (-A * BZ + BX * G) + const
    ) / denom

    if (B == 0 or BZ == 0) and (BY == 0 or G == 0):
        const1 = math.sqrt(
            G * G * (-A * A * X * X + (B * B + G * G) * (L - X) * (L + X))
        )
        Y = ((-A * B * X) + const1) / (B * B + G * G)
        Z = -(A * G * G * X + B * const1) / (G * (B * B + G * G))
    else:
        Y = (
            (A * A * BY * F) * (B * BZ - BY * G)
            + G * (-F * math.pow(B * BZ - BY * G, 2) + BX * const)
            - A * (B * B * BX * BZ * F - B * BX * BY * F * G + BZ * const)
        ) / ((B * BZ - BY * G) * denom)
        Z = (
            (A * A * BZ * F) * (B * BZ - BY * G)
            + (B * F) * math.pow(B * BZ - BY * G, 2)
            + (A * BX * F * G) * (-B * BZ + BY * G)
            - B * BX * const
            + A * BY * const
        ) / ((B * BZ - BY * G) * denom)

    # Get the new Vector from the origin
    D = Vector(X, Y, Z) + CV
    with warnings.catch_warnings():
        # ignore inconsequential warning
        warnings.simplefilter("ignore")
        temp = calc_dihedral(AV, BV, CV, D) * (180.0 / math.pi)

    di = di - temp
    rot = rotaxis(math.pi * (di / 180.0), CV - BV)
    D = (D - BV).left_multiply(rot) + BV

    return D.get_array()


def makeGly(segID: int, N, CA, C, O, geo: Geo) -> Residue:
    """Creates a Glycine residue"""
    res = Residue((" ", segID, " "), "GLY", "    ")

    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    return res


def makeAce(segID: int, N, CA, C, O, geo: AceGeo) -> Residue:
    """Creates an ACE capping residue"""
    res = makeGly(segID, N, CA, C, O, geo)
    res.resname = "ACE"
    return res


def makeNme(segID: int, N, CA, C, O, geo: NmeGeo) -> Residue:
    """Creates a NME capping residue"""
    res = makeGly(segID, N, CA, C, O, geo)
    res.resname = "NME"
    return res


def makeAla(segID: int, N, CA, C, O, geo: AlaGeo) -> Residue:
    """Creates an Alanine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")

    res = Residue((" ", segID, " "), "ALA", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    return res


def makeSer(segID: int, N, CA, C, O, geo: SerGeo) -> Residue:
    """Creates a Serine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_OG_length = geo.CB_OG_length
    CA_CB_OG_angle = geo.CA_CB_OG_angle
    N_CA_CB_OG_diangle = geo.N_CA_CB_OG_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    oxygen_g = calculateCoordinates(
        N, CA, CB, CB_OG_length, CA_CB_OG_angle, N_CA_CB_OG_diangle
    )
    OG = Atom("OG", oxygen_g, 0.0, 1.0, " ", " OG", 0, "O")

    ##Create Reside Data Structure
    res = Residue((" ", segID, " "), "SER", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(OG)
    return res


def makeCys(segID: int, N, CA, C, O, geo: CysGeo) -> Residue:
    """Creates a Cysteine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_SG_length = geo.CB_SG_length
    CA_CB_SG_angle = geo.CA_CB_SG_angle
    N_CA_CB_SG_diangle = geo.N_CA_CB_SG_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    sulfur_g = calculateCoordinates(
        N, CA, CB, CB_SG_length, CA_CB_SG_angle, N_CA_CB_SG_diangle
    )
    SG = Atom("SG", sulfur_g, 0.0, 1.0, " ", " SG", 0, "S")

    res = Residue((" ", segID, " "), "CYS", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(SG)
    return res


def makeVal(segID: int, N, CA, C, O, geo: ValGeo) -> Residue:
    """Creates a Valine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG1_length = geo.CB_CG1_length
    CA_CB_CG1_angle = geo.CA_CB_CG1_angle
    N_CA_CB_CG1_diangle = geo.N_CA_CB_CG1_diangle

    CB_CG2_length = geo.CB_CG2_length
    CA_CB_CG2_angle = geo.CA_CB_CG2_angle
    N_CA_CB_CG2_diangle = geo.N_CA_CB_CG2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g1 = calculateCoordinates(
        N, CA, CB, CB_CG1_length, CA_CB_CG1_angle, N_CA_CB_CG1_diangle
    )
    CG1 = Atom("CG1", carbon_g1, 0.0, 1.0, " ", " CG1", 0, "C")
    carbon_g2 = calculateCoordinates(
        N, CA, CB, CB_CG2_length, CA_CB_CG2_angle, N_CA_CB_CG2_diangle
    )
    CG2 = Atom("CG2", carbon_g2, 0.0, 1.0, " ", " CG2", 0, "C")

    res = Residue((" ", segID, " "), "VAL", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG1)
    res.add(CG2)
    return res


def makeIle(segID: int, N, CA, C, O, geo: IleGeo) -> Residue:
    """Creates an Isoleucine residue"""
    ##R-group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG1_length = geo.CB_CG1_length
    CA_CB_CG1_angle = geo.CA_CB_CG1_angle
    N_CA_CB_CG1_diangle = geo.N_CA_CB_CG1_diangle

    CB_CG2_length = geo.CB_CG2_length
    CA_CB_CG2_angle = geo.CA_CB_CG2_angle
    N_CA_CB_CG2_diangle = geo.N_CA_CB_CG2_diangle

    CG1_CD1_length = geo.CG1_CD1_length
    CB_CG1_CD1_angle = geo.CB_CG1_CD1_angle
    CA_CB_CG1_CD1_diangle = geo.CA_CB_CG1_CD1_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g1 = calculateCoordinates(
        N, CA, CB, CB_CG1_length, CA_CB_CG1_angle, N_CA_CB_CG1_diangle
    )
    CG1 = Atom("CG1", carbon_g1, 0.0, 1.0, " ", " CG1", 0, "C")
    carbon_g2 = calculateCoordinates(
        N, CA, CB, CB_CG2_length, CA_CB_CG2_angle, N_CA_CB_CG2_diangle
    )
    CG2 = Atom("CG2", carbon_g2, 0.0, 1.0, " ", " CG2", 0, "C")
    carbon_d1 = calculateCoordinates(
        CA, CB, CG1, CG1_CD1_length, CB_CG1_CD1_angle, CA_CB_CG1_CD1_diangle
    )
    CD1 = Atom("CD1", carbon_d1, 0.0, 1.0, " ", " CD1", 0, "C")

    res = Residue((" ", segID, " "), "ILE", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG1)
    res.add(CG2)
    res.add(CD1)
    return res


def makeLeu(segID: int, N, CA, C, O, geo: LeuGeo) -> Residue:
    """Creates a Leucine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_CD1_length = geo.CG_CD1_length
    CB_CG_CD1_angle = geo.CB_CG_CD1_angle
    CA_CB_CG_CD1_diangle = geo.CA_CB_CG_CD1_diangle

    CG_CD2_length = geo.CG_CD2_length
    CB_CG_CD2_angle = geo.CB_CG_CD2_angle
    CA_CB_CG_CD2_diangle = geo.CA_CB_CG_CD2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g1 = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g1, 0.0, 1.0, " ", " CG", 0, "C")
    carbon_d1 = calculateCoordinates(
        CA, CB, CG, CG_CD1_length, CB_CG_CD1_angle, CA_CB_CG_CD1_diangle
    )
    CD1 = Atom("CD1", carbon_d1, 0.0, 1.0, " ", " CD1", 0, "C")
    carbon_d2 = calculateCoordinates(
        CA, CB, CG, CG_CD2_length, CB_CG_CD2_angle, CA_CB_CG_CD2_diangle
    )
    CD2 = Atom("CD2", carbon_d2, 0.0, 1.0, " ", " CD2", 0, "C")

    res = Residue((" ", segID, " "), "LEU", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(CD1)
    res.add(CD2)
    return res


def makeThr(segID: int, N, CA, C, O, geo: ThrGeo) -> Residue:
    """Creates a Threonine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_OG1_length = geo.CB_OG1_length
    CA_CB_OG1_angle = geo.CA_CB_OG1_angle
    N_CA_CB_OG1_diangle = geo.N_CA_CB_OG1_diangle

    CB_CG2_length = geo.CB_CG2_length
    CA_CB_CG2_angle = geo.CA_CB_CG2_angle
    N_CA_CB_CG2_diangle = geo.N_CA_CB_CG2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    oxygen_g1 = calculateCoordinates(
        N, CA, CB, CB_OG1_length, CA_CB_OG1_angle, N_CA_CB_OG1_diangle
    )
    OG1 = Atom("OG1", oxygen_g1, 0.0, 1.0, " ", " OG1", 0, "O")
    carbon_g2 = calculateCoordinates(
        N, CA, CB, CB_CG2_length, CA_CB_CG2_angle, N_CA_CB_CG2_diangle
    )
    CG2 = Atom("CG2", carbon_g2, 0.0, 1.0, " ", " CG2", 0, "C")

    res = Residue((" ", segID, " "), "THR", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(OG1)
    res.add(CG2)
    return res


def makeArg(segID: int, N, CA, C, O, geo: ArgGeo) -> Residue:
    """Creates an Arginie residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_CD_length = geo.CG_CD_length
    CB_CG_CD_angle = geo.CB_CG_CD_angle
    CA_CB_CG_CD_diangle = geo.CA_CB_CG_CD_diangle

    CD_NE_length = geo.CD_NE_length
    CG_CD_NE_angle = geo.CG_CD_NE_angle
    CB_CG_CD_NE_diangle = geo.CB_CG_CD_NE_diangle

    NE_CZ_length = geo.NE_CZ_length
    CD_NE_CZ_angle = geo.CD_NE_CZ_angle
    CG_CD_NE_CZ_diangle = geo.CG_CD_NE_CZ_diangle

    CZ_NH1_length = geo.CZ_NH1_length
    NE_CZ_NH1_angle = geo.NE_CZ_NH1_angle
    CD_NE_CZ_NH1_diangle = geo.CD_NE_CZ_NH1_diangle

    CZ_NH2_length = geo.CZ_NH2_length
    NE_CZ_NH2_angle = geo.NE_CZ_NH2_angle
    CD_NE_CZ_NH2_diangle = geo.CD_NE_CZ_NH2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    carbon_d = calculateCoordinates(
        CA, CB, CG, CG_CD_length, CB_CG_CD_angle, CA_CB_CG_CD_diangle
    )
    CD = Atom("CD", carbon_d, 0.0, 1.0, " ", " CD", 0, "C")
    nitrogen_e = calculateCoordinates(
        CB, CG, CD, CD_NE_length, CG_CD_NE_angle, CB_CG_CD_NE_diangle
    )
    NE = Atom("NE", nitrogen_e, 0.0, 1.0, " ", " NE", 0, "N")
    carbon_z = calculateCoordinates(
        CG, CD, NE, NE_CZ_length, CD_NE_CZ_angle, CG_CD_NE_CZ_diangle
    )
    CZ = Atom("CZ", carbon_z, 0.0, 1.0, " ", " CZ", 0, "C")
    nitrogen_h1 = calculateCoordinates(
        CD, NE, CZ, CZ_NH1_length, NE_CZ_NH1_angle, CD_NE_CZ_NH1_diangle
    )
    NH1 = Atom("NH1", nitrogen_h1, 0.0, 1.0, " ", " NH1", 0, "N")
    nitrogen_h2 = calculateCoordinates(
        CD, NE, CZ, CZ_NH2_length, NE_CZ_NH2_angle, CD_NE_CZ_NH2_diangle
    )
    NH2 = Atom("NH2", nitrogen_h2, 0.0, 1.0, " ", " NH2", 0, "N")

    res = Residue((" ", segID, " "), "ARG", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(CD)
    res.add(NE)
    res.add(CZ)
    res.add(NH1)
    res.add(NH2)
    return res


def makeLys(segID: int, N, CA, C, O, geo: LysGeo) -> Residue:
    """Creates a Lysine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_CD_length = geo.CG_CD_length
    CB_CG_CD_angle = geo.CB_CG_CD_angle
    CA_CB_CG_CD_diangle = geo.CA_CB_CG_CD_diangle

    CD_CE_length = geo.CD_CE_length
    CG_CD_CE_angle = geo.CG_CD_CE_angle
    CB_CG_CD_CE_diangle = geo.CB_CG_CD_CE_diangle

    CE_NZ_length = geo.CE_NZ_length
    CD_CE_NZ_angle = geo.CD_CE_NZ_angle
    CG_CD_CE_NZ_diangle = geo.CG_CD_CE_NZ_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    carbon_d = calculateCoordinates(
        CA, CB, CG, CG_CD_length, CB_CG_CD_angle, CA_CB_CG_CD_diangle
    )
    CD = Atom("CD", carbon_d, 0.0, 1.0, " ", " CD", 0, "C")
    carbon_e = calculateCoordinates(
        CB, CG, CD, CD_CE_length, CG_CD_CE_angle, CB_CG_CD_CE_diangle
    )
    CE = Atom("CE", carbon_e, 0.0, 1.0, " ", " CE", 0, "C")
    nitrogen_z = calculateCoordinates(
        CG, CD, CE, CE_NZ_length, CD_CE_NZ_angle, CG_CD_CE_NZ_diangle
    )
    NZ = Atom("NZ", nitrogen_z, 0.0, 1.0, " ", " NZ", 0, "N")

    res = Residue((" ", segID, " "), "LYS", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(CD)
    res.add(CE)
    res.add(NZ)
    return res


def makeAsp(segID: int, N, CA, C, O, geo: AspGeo) -> Residue:
    """Creates an Aspartic Acid residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_OD1_length = geo.CG_OD1_length
    CB_CG_OD1_angle = geo.CB_CG_OD1_angle
    CA_CB_CG_OD1_diangle = geo.CA_CB_CG_OD1_diangle

    CG_OD2_length = geo.CG_OD2_length
    CB_CG_OD2_angle = geo.CB_CG_OD2_angle
    CA_CB_CG_OD2_diangle = geo.CA_CB_CG_OD2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    oxygen_d1 = calculateCoordinates(
        CA, CB, CG, CG_OD1_length, CB_CG_OD1_angle, CA_CB_CG_OD1_diangle
    )
    OD1 = Atom("OD1", oxygen_d1, 0.0, 1.0, " ", " OD1", 0, "O")
    oxygen_d2 = calculateCoordinates(
        CA, CB, CG, CG_OD2_length, CB_CG_OD2_angle, CA_CB_CG_OD2_diangle
    )
    OD2 = Atom("OD2", oxygen_d2, 0.0, 1.0, " ", " OD2", 0, "O")

    res = Residue((" ", segID, " "), "ASP", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(OD1)
    res.add(OD2)
    return res


def makeAsn(segID, N, CA, C, O, geo):
    """Creates an Asparagine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_OD1_length = geo.CG_OD1_length
    CB_CG_OD1_angle = geo.CB_CG_OD1_angle
    CA_CB_CG_OD1_diangle = geo.CA_CB_CG_OD1_diangle

    CG_ND2_length = geo.CG_ND2_length
    CB_CG_ND2_angle = geo.CB_CG_ND2_angle
    CA_CB_CG_ND2_diangle = geo.CA_CB_CG_ND2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    oxygen_d1 = calculateCoordinates(
        CA, CB, CG, CG_OD1_length, CB_CG_OD1_angle, CA_CB_CG_OD1_diangle
    )
    OD1 = Atom("OD1", oxygen_d1, 0.0, 1.0, " ", " OD1", 0, "O")
    nitrogen_d2 = calculateCoordinates(
        CA, CB, CG, CG_ND2_length, CB_CG_ND2_angle, CA_CB_CG_ND2_diangle
    )
    ND2 = Atom("ND2", nitrogen_d2, 0.0, 1.0, " ", " ND2", 0, "N")
    res = Residue((" ", segID, " "), "ASN", "    ")

    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(OD1)
    res.add(ND2)
    return res


def makeGlu(segID: int, N, CA, C, O, geo: GluGeo) -> Residue:
    """Creates a Glutamic Acid residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_CD_length = geo.CG_CD_length
    CB_CG_CD_angle = geo.CB_CG_CD_angle
    CA_CB_CG_CD_diangle = geo.CA_CB_CG_CD_diangle

    CD_OE1_length = geo.CD_OE1_length
    CG_CD_OE1_angle = geo.CG_CD_OE1_angle
    CB_CG_CD_OE1_diangle = geo.CB_CG_CD_OE1_diangle

    CD_OE2_length = geo.CD_OE2_length
    CG_CD_OE2_angle = geo.CG_CD_OE2_angle
    CB_CG_CD_OE2_diangle = geo.CB_CG_CD_OE2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    carbon_d = calculateCoordinates(
        CA, CB, CG, CG_CD_length, CB_CG_CD_angle, CA_CB_CG_CD_diangle
    )
    CD = Atom("CD", carbon_d, 0.0, 1.0, " ", " CD", 0, "C")
    oxygen_e1 = calculateCoordinates(
        CB, CG, CD, CD_OE1_length, CG_CD_OE1_angle, CB_CG_CD_OE1_diangle
    )
    OE1 = Atom("OE1", oxygen_e1, 0.0, 1.0, " ", " OE1", 0, "O")
    oxygen_e2 = calculateCoordinates(
        CB, CG, CD, CD_OE2_length, CG_CD_OE2_angle, CB_CG_CD_OE2_diangle
    )
    OE2 = Atom("OE2", oxygen_e2, 0.0, 1.0, " ", " OE2", 0, "O")

    res = Residue((" ", segID, " "), "GLU", "    ")

    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(CD)
    res.add(OE1)
    res.add(OE2)
    return res


def makeGln(segID: int, N, CA, C, O, geo: GlnGeo) -> Residue:
    """Creates a Glutamine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_CD_length = geo.CG_CD_length
    CB_CG_CD_angle = geo.CB_CG_CD_angle
    CA_CB_CG_CD_diangle = geo.CA_CB_CG_CD_diangle

    CD_OE1_length = geo.CD_OE1_length
    CG_CD_OE1_angle = geo.CG_CD_OE1_angle
    CB_CG_CD_OE1_diangle = geo.CB_CG_CD_OE1_diangle

    CD_NE2_length = geo.CD_NE2_length
    CG_CD_NE2_angle = geo.CG_CD_NE2_angle
    CB_CG_CD_NE2_diangle = geo.CB_CG_CD_NE2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    carbon_d = calculateCoordinates(
        CA, CB, CG, CG_CD_length, CB_CG_CD_angle, CA_CB_CG_CD_diangle
    )
    CD = Atom("CD", carbon_d, 0.0, 1.0, " ", " CD", 0, "C")
    oxygen_e1 = calculateCoordinates(
        CB, CG, CD, CD_OE1_length, CG_CD_OE1_angle, CB_CG_CD_OE1_diangle
    )
    OE1 = Atom("OE1", oxygen_e1, 0.0, 1.0, " ", " OE1", 0, "O")
    nitrogen_e2 = calculateCoordinates(
        CB, CG, CD, CD_NE2_length, CG_CD_NE2_angle, CB_CG_CD_NE2_diangle
    )
    NE2 = Atom("NE2", nitrogen_e2, 0.0, 1.0, " ", " NE2", 0, "N")

    ##Create Residue DS
    res = Residue((" ", segID, " "), "GLN", "    ")

    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(CD)
    res.add(OE1)
    res.add(NE2)
    return res


def makeMet(segID: int, N, CA, C, O, geo: MetGeo) -> Residue:
    """Creates a Methionine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_SD_length = geo.CG_SD_length
    CB_CG_SD_angle = geo.CB_CG_SD_angle
    CA_CB_CG_SD_diangle = geo.CA_CB_CG_SD_diangle

    SD_CE_length = geo.SD_CE_length
    CG_SD_CE_angle = geo.CG_SD_CE_angle
    CB_CG_SD_CE_diangle = geo.CB_CG_SD_CE_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    sulfur_d = calculateCoordinates(
        CA, CB, CG, CG_SD_length, CB_CG_SD_angle, CA_CB_CG_SD_diangle
    )
    SD = Atom("SD", sulfur_d, 0.0, 1.0, " ", " SD", 0, "S")
    carbon_e = calculateCoordinates(
        CB, CG, SD, SD_CE_length, CG_SD_CE_angle, CB_CG_SD_CE_diangle
    )
    CE = Atom("CE", carbon_e, 0.0, 1.0, " ", " CE", 0, "C")

    res = Residue((" ", segID, " "), "MET", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(SD)
    res.add(CE)
    return res


def makeHis(segID: int, N, CA, C, O, geo: HisGeo) -> Residue:
    """Creates a Histidine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_ND1_length = geo.CG_ND1_length
    CB_CG_ND1_angle = geo.CB_CG_ND1_angle
    CA_CB_CG_ND1_diangle = geo.CA_CB_CG_ND1_diangle

    CG_CD2_length = geo.CG_CD2_length
    CB_CG_CD2_angle = geo.CB_CG_CD2_angle
    CA_CB_CG_CD2_diangle = geo.CA_CB_CG_CD2_diangle

    ND1_CE1_length = geo.ND1_CE1_length
    CG_ND1_CE1_angle = geo.CG_ND1_CE1_angle
    CB_CG_ND1_CE1_diangle = geo.CB_CG_ND1_CE1_diangle

    CD2_NE2_length = geo.CD2_NE2_length
    CG_CD2_NE2_angle = geo.CG_CD2_NE2_angle
    CB_CG_CD2_NE2_diangle = geo.CB_CG_CD2_NE2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    nitrogen_d1 = calculateCoordinates(
        CA, CB, CG, CG_ND1_length, CB_CG_ND1_angle, CA_CB_CG_ND1_diangle
    )
    ND1 = Atom("ND1", nitrogen_d1, 0.0, 1.0, " ", " ND1", 0, "N")
    carbon_d2 = calculateCoordinates(
        CA, CB, CG, CG_CD2_length, CB_CG_CD2_angle, CA_CB_CG_CD2_diangle
    )
    CD2 = Atom("CD2", carbon_d2, 0.0, 1.0, " ", " CD2", 0, "C")
    carbon_e1 = calculateCoordinates(
        CB, CG, ND1, ND1_CE1_length, CG_ND1_CE1_angle, CB_CG_ND1_CE1_diangle
    )
    CE1 = Atom("CE1", carbon_e1, 0.0, 1.0, " ", " CE1", 0, "C")
    nitrogen_e2 = calculateCoordinates(
        CB, CG, CD2, CD2_NE2_length, CG_CD2_NE2_angle, CB_CG_CD2_NE2_diangle
    )
    NE2 = Atom("NE2", nitrogen_e2, 0.0, 1.0, " ", " NE2", 0, "N")

    res = Residue((" ", segID, " "), "HIS", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(ND1)
    res.add(CD2)
    res.add(CE1)
    res.add(NE2)
    return res


def makePro(segID: int, N, CA, C, O, geo: ProGeo) -> Residue:
    """Creates a Proline residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_CD_length = geo.CG_CD_length
    CB_CG_CD_angle = geo.CB_CG_CD_angle
    CA_CB_CG_CD_diangle = geo.CA_CB_CG_CD_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    carbon_d = calculateCoordinates(
        CA, CB, CG, CG_CD_length, CB_CG_CD_angle, CA_CB_CG_CD_diangle
    )
    CD = Atom("CD", carbon_d, 0.0, 1.0, " ", " CD", 0, "C")

    res = Residue((" ", segID, " "), "PRO", "    ")

    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(CD)

    return res


def makePhe(segID: int, N, CA, C, O, geo: PheGeo) -> Residue:
    """Creates a Phenylalanine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_CD1_length = geo.CG_CD1_length
    CB_CG_CD1_angle = geo.CB_CG_CD1_angle
    CA_CB_CG_CD1_diangle = geo.CA_CB_CG_CD1_diangle

    CG_CD2_length = geo.CG_CD2_length
    CB_CG_CD2_angle = geo.CB_CG_CD2_angle
    CA_CB_CG_CD2_diangle = geo.CA_CB_CG_CD2_diangle

    CD1_CE1_length = geo.CD1_CE1_length
    CG_CD1_CE1_angle = geo.CG_CD1_CE1_angle
    CB_CG_CD1_CE1_diangle = geo.CB_CG_CD1_CE1_diangle

    CD2_CE2_length = geo.CD2_CE2_length
    CG_CD2_CE2_angle = geo.CG_CD2_CE2_angle
    CB_CG_CD2_CE2_diangle = geo.CB_CG_CD2_CE2_diangle

    CE1_CZ_length = geo.CE1_CZ_length
    CD1_CE1_CZ_angle = geo.CD1_CE1_CZ_angle
    CG_CD1_CE1_CZ_diangle = geo.CG_CD1_CE1_CZ_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    carbon_d1 = calculateCoordinates(
        CA, CB, CG, CG_CD1_length, CB_CG_CD1_angle, CA_CB_CG_CD1_diangle
    )
    CD1 = Atom("CD1", carbon_d1, 0.0, 1.0, " ", " CD1", 0, "C")
    carbon_d2 = calculateCoordinates(
        CA, CB, CG, CG_CD2_length, CB_CG_CD2_angle, CA_CB_CG_CD2_diangle
    )
    CD2 = Atom("CD2", carbon_d2, 0.0, 1.0, " ", " CD2", 0, "C")
    carbon_e1 = calculateCoordinates(
        CB, CG, CD1, CD1_CE1_length, CG_CD1_CE1_angle, CB_CG_CD1_CE1_diangle
    )
    CE1 = Atom("CE1", carbon_e1, 0.0, 1.0, " ", " CE1", 0, "C")
    carbon_e2 = calculateCoordinates(
        CB, CG, CD2, CD2_CE2_length, CG_CD2_CE2_angle, CB_CG_CD2_CE2_diangle
    )
    CE2 = Atom("CE2", carbon_e2, 0.0, 1.0, " ", " CE2", 0, "C")
    carbon_z = calculateCoordinates(
        CG, CD1, CE1, CE1_CZ_length, CD1_CE1_CZ_angle, CG_CD1_CE1_CZ_diangle
    )
    CZ = Atom("CZ", carbon_z, 0.0, 1.0, " ", " CZ", 0, "C")

    res = Residue((" ", segID, " "), "PHE", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(CD1)
    res.add(CE1)
    res.add(CD2)
    res.add(CE2)
    res.add(CZ)
    return res


def makeTyr(segID: int, N, CA, C, O, geo: TyrGeo) -> Residue:
    """Creates a Tyrosine residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_CD1_length = geo.CG_CD1_length
    CB_CG_CD1_angle = geo.CB_CG_CD1_angle
    CA_CB_CG_CD1_diangle = geo.CA_CB_CG_CD1_diangle

    CG_CD2_length = geo.CG_CD2_length
    CB_CG_CD2_angle = geo.CB_CG_CD2_angle
    CA_CB_CG_CD2_diangle = geo.CA_CB_CG_CD2_diangle

    CD1_CE1_length = geo.CD1_CE1_length
    CG_CD1_CE1_angle = geo.CG_CD1_CE1_angle
    CB_CG_CD1_CE1_diangle = geo.CB_CG_CD1_CE1_diangle

    CD2_CE2_length = geo.CD2_CE2_length
    CG_CD2_CE2_angle = geo.CG_CD2_CE2_angle
    CB_CG_CD2_CE2_diangle = geo.CB_CG_CD2_CE2_diangle

    CE1_CZ_length = geo.CE1_CZ_length
    CD1_CE1_CZ_angle = geo.CD1_CE1_CZ_angle
    CG_CD1_CE1_CZ_diangle = geo.CG_CD1_CE1_CZ_diangle

    CZ_OH_length = geo.CZ_OH_length
    CE1_CZ_OH_angle = geo.CE1_CZ_OH_angle
    CD1_CE1_CZ_OH_diangle = geo.CD1_CE1_CZ_OH_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    carbon_d1 = calculateCoordinates(
        CA, CB, CG, CG_CD1_length, CB_CG_CD1_angle, CA_CB_CG_CD1_diangle
    )
    CD1 = Atom("CD1", carbon_d1, 0.0, 1.0, " ", " CD1", 0, "C")
    carbon_d2 = calculateCoordinates(
        CA, CB, CG, CG_CD2_length, CB_CG_CD2_angle, CA_CB_CG_CD2_diangle
    )
    CD2 = Atom("CD2", carbon_d2, 0.0, 1.0, " ", " CD2", 0, "C")
    carbon_e1 = calculateCoordinates(
        CB, CG, CD1, CD1_CE1_length, CG_CD1_CE1_angle, CB_CG_CD1_CE1_diangle
    )
    CE1 = Atom("CE1", carbon_e1, 0.0, 1.0, " ", " CE1", 0, "C")
    carbon_e2 = calculateCoordinates(
        CB, CG, CD2, CD2_CE2_length, CG_CD2_CE2_angle, CB_CG_CD2_CE2_diangle
    )
    CE2 = Atom("CE2", carbon_e2, 0.0, 1.0, " ", " CE2", 0, "C")
    carbon_z = calculateCoordinates(
        CG, CD1, CE1, CE1_CZ_length, CD1_CE1_CZ_angle, CG_CD1_CE1_CZ_diangle
    )
    CZ = Atom("CZ", carbon_z, 0.0, 1.0, " ", " CZ", 0, "C")
    oxygen_h = calculateCoordinates(
        CD1, CE1, CZ, CZ_OH_length, CE1_CZ_OH_angle, CD1_CE1_CZ_OH_diangle
    )
    OH = Atom("OH", oxygen_h, 0.0, 1.0, " ", " OH", 0, "O")

    ##Create Residue Data S
    res = Residue((" ", segID, " "), "TYR", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(CD1)
    res.add(CE1)
    res.add(CD2)
    res.add(CE2)
    res.add(CZ)
    res.add(OH)
    return res


def makeTrp(segID: int, N, CA, C, O, geo: TrpGeo) -> Residue:
    """Creates a Tryptophan residue"""
    ##R-Group
    CA_CB_length = geo.CA_CB_length
    C_CA_CB_angle = geo.C_CA_CB_angle
    N_C_CA_CB_diangle = geo.N_C_CA_CB_diangle

    CB_CG_length = geo.CB_CG_length
    CA_CB_CG_angle = geo.CA_CB_CG_angle
    N_CA_CB_CG_diangle = geo.N_CA_CB_CG_diangle

    CG_CD1_length = geo.CG_CD1_length
    CB_CG_CD1_angle = geo.CB_CG_CD1_angle
    CA_CB_CG_CD1_diangle = geo.CA_CB_CG_CD1_diangle

    CG_CD2_length = geo.CG_CD2_length
    CB_CG_CD2_angle = geo.CB_CG_CD2_angle
    CA_CB_CG_CD2_diangle = geo.CA_CB_CG_CD2_diangle

    CD1_NE1_length = geo.CD1_NE1_length
    CG_CD1_NE1_angle = geo.CG_CD1_NE1_angle
    CB_CG_CD1_NE1_diangle = geo.CB_CG_CD1_NE1_diangle

    CD2_CE2_length = geo.CD2_CE2_length
    CG_CD2_CE2_angle = geo.CG_CD2_CE2_angle
    CB_CG_CD2_CE2_diangle = geo.CB_CG_CD2_CE2_diangle

    CD2_CE3_length = geo.CD2_CE3_length
    CG_CD2_CE3_angle = geo.CG_CD2_CE3_angle
    CB_CG_CD2_CE3_diangle = geo.CB_CG_CD2_CE3_diangle

    CE2_CZ2_length = geo.CE2_CZ2_length
    CD2_CE2_CZ2_angle = geo.CD2_CE2_CZ2_angle
    CG_CD2_CE2_CZ2_diangle = geo.CG_CD2_CE2_CZ2_diangle

    CE3_CZ3_length = geo.CE3_CZ3_length
    CD2_CE3_CZ3_angle = geo.CD2_CE3_CZ3_angle
    CG_CD2_CE3_CZ3_diangle = geo.CG_CD2_CE3_CZ3_diangle

    CZ2_CH2_length = geo.CZ2_CH2_length
    CE2_CZ2_CH2_angle = geo.CE2_CZ2_CH2_angle
    CD2_CE2_CZ2_CH2_diangle = geo.CD2_CE2_CZ2_CH2_diangle

    carbon_b = calculateCoordinates(
        N, C, CA, CA_CB_length, C_CA_CB_angle, N_C_CA_CB_diangle
    )
    CB = Atom("CB", carbon_b, 0.0, 1.0, " ", " CB", 0, "C")
    carbon_g = calculateCoordinates(
        N, CA, CB, CB_CG_length, CA_CB_CG_angle, N_CA_CB_CG_diangle
    )
    CG = Atom("CG", carbon_g, 0.0, 1.0, " ", " CG", 0, "C")
    carbon_d1 = calculateCoordinates(
        CA, CB, CG, CG_CD1_length, CB_CG_CD1_angle, CA_CB_CG_CD1_diangle
    )
    CD1 = Atom("CD1", carbon_d1, 0.0, 1.0, " ", " CD1", 0, "C")
    carbon_d2 = calculateCoordinates(
        CA, CB, CG, CG_CD2_length, CB_CG_CD2_angle, CA_CB_CG_CD2_diangle
    )
    CD2 = Atom("CD2", carbon_d2, 0.0, 1.0, " ", " CD2", 0, "C")
    nitrogen_e1 = calculateCoordinates(
        CB, CG, CD1, CD1_NE1_length, CG_CD1_NE1_angle, CB_CG_CD1_NE1_diangle
    )
    NE1 = Atom("NE1", nitrogen_e1, 0.0, 1.0, " ", " NE1", 0, "N")
    carbon_e2 = calculateCoordinates(
        CB, CG, CD2, CD2_CE2_length, CG_CD2_CE2_angle, CB_CG_CD2_CE2_diangle
    )
    CE2 = Atom("CE2", carbon_e2, 0.0, 1.0, " ", " CE2", 0, "C")
    carbon_e3 = calculateCoordinates(
        CB, CG, CD2, CD2_CE3_length, CG_CD2_CE3_angle, CB_CG_CD2_CE3_diangle
    )
    CE3 = Atom("CE3", carbon_e3, 0.0, 1.0, " ", " CE3", 0, "C")

    carbon_z2 = calculateCoordinates(
        CG, CD2, CE2, CE2_CZ2_length, CD2_CE2_CZ2_angle, CG_CD2_CE2_CZ2_diangle
    )
    CZ2 = Atom("CZ2", carbon_z2, 0.0, 1.0, " ", " CZ2", 0, "C")

    carbon_z3 = calculateCoordinates(
        CG, CD2, CE3, CE3_CZ3_length, CD2_CE3_CZ3_angle, CG_CD2_CE3_CZ3_diangle
    )
    CZ3 = Atom("CZ3", carbon_z3, 0.0, 1.0, " ", " CZ3", 0, "C")

    carbon_h2 = calculateCoordinates(
        CD2, CE2, CZ2, CZ2_CH2_length, CE2_CZ2_CH2_angle, CD2_CE2_CZ2_CH2_diangle
    )
    CH2 = Atom("CH2", carbon_h2, 0.0, 1.0, " ", " CH2", 0, "C")

    ##Create Residue DS
    res = Residue((" ", segID, " "), "TRP", "    ")
    res.add(N)
    res.add(CA)
    res.add(C)
    res.add(O)
    res.add(CB)
    res.add(CG)
    res.add(CD1)
    res.add(CD2)

    res.add(NE1)
    res.add(CE2)
    res.add(CE3)

    res.add(CZ2)
    res.add(CZ3)

    res.add(CH2)
    return res


def make_res_of_type(segID: int, N, CA, C, O, geo: Geo) -> Residue:
    if isinstance(geo, AceGeo):
        res = makeAce(segID, N, CA, C, O, geo)
    elif isinstance(geo, NmeGeo):
        res = makeNme(segID, N, CA, C, O, geo)
    elif isinstance(geo, GlyGeo) or isinstance(geo, DGlyGeo):
        res = makeGly(segID, N, CA, C, O, geo)
    elif isinstance(geo, AlaGeo) or isinstance(geo, DAlaGeo):
        res = makeAla(segID, N, CA, C, O, geo)
    elif isinstance(geo, SerGeo) or isinstance(geo, DSerGeo):
        res = makeSer(segID, N, CA, C, O, geo)
    elif isinstance(geo, CysGeo) or isinstance(geo, DCysGeo):
        res = makeCys(segID, N, CA, C, O, geo)
    elif isinstance(geo, ValGeo) or isinstance(geo, DValGeo):
        res = makeVal(segID, N, CA, C, O, geo)
    elif isinstance(geo, IleGeo) or isinstance(geo, DIleGeo):
        res = makeIle(segID, N, CA, C, O, geo)
    elif isinstance(geo, LeuGeo) or isinstance(geo, DLeuGeo):
        res = makeLeu(segID, N, CA, C, O, geo)
    elif isinstance(geo, ThrGeo) or isinstance(geo, DThrGeo):
        res = makeThr(segID, N, CA, C, O, geo)
    elif isinstance(geo, ArgGeo) or isinstance(geo, DArgGeo):
        res = makeArg(segID, N, CA, C, O, geo)
    elif isinstance(geo, LysGeo) or isinstance(geo, DLysGeo):
        res = makeLys(segID, N, CA, C, O, geo)
    elif isinstance(geo, AspGeo) or isinstance(geo, DAspGeo):
        res = makeAsp(segID, N, CA, C, O, geo)
    elif isinstance(geo, GluGeo) or isinstance(geo, DGluGeo):
        res = makeGlu(segID, N, CA, C, O, geo)
    elif isinstance(geo, AsnGeo) or isinstance(geo, DAsnGeo):
        res = makeAsn(segID, N, CA, C, O, geo)
    elif isinstance(geo, GlnGeo) or isinstance(geo, DGlnGeo):
        res = makeGln(segID, N, CA, C, O, geo)
    elif isinstance(geo, MetGeo) or isinstance(geo, DMetGeo):
        res = makeMet(segID, N, CA, C, O, geo)
    elif isinstance(geo, HisGeo) or isinstance(geo, DHisGeo):
        res = makeHis(segID, N, CA, C, O, geo)
    elif isinstance(geo, ProGeo) or isinstance(geo, DProGeo):
        res = makePro(segID, N, CA, C, O, geo)
    elif isinstance(geo, PheGeo) or isinstance(geo, DPheGeo):
        res = makePhe(segID, N, CA, C, O, geo)
    elif isinstance(geo, TyrGeo) or isinstance(geo, DTyrGeo):
        res = makeTyr(segID, N, CA, C, O, geo)
    elif isinstance(geo, TrpGeo) or isinstance(geo, DTrpGeo):
        res = makeTrp(segID, N, CA, C, O, geo)
    else:
        res = makeGly(segID, N, CA, C, O, geo)
    return res


def initialize_res(residue: Union[Geo, str]) -> Structure:
    """Creates a new structure containing a single amino acid. The type and
    geometry of the amino acid are determined by the argument, which has to be
    either a geometry object or a single-letter amino acid code.
    The amino acid will be placed into chain A of model 0."""

    if isinstance(residue, Geo):
        geo = residue
    elif isinstance(residue, str):
        geo = geometry(residue)
    else:
        raise ValueError("Invalid residue argument:", residue)

    segID = 1
    AA = geo.residue_name
    CA_N_length = geo.CA_N_length
    CA_C_length = geo.CA_C_length
    N_CA_C_angle = geo.N_CA_C_angle

    CA_coord = np.array([0.0, 0.0, 0.0])
    C_coord = np.array([CA_C_length, 0, 0])
    N_coord = np.array(
        [
            CA_N_length * math.cos(N_CA_C_angle * (math.pi / 180.0)),
            CA_N_length * math.sin(N_CA_C_angle * (math.pi / 180.0)),
            0,
        ]
    )

    N = Atom("N", N_coord, 0.0, 1.0, " ", " N", 0, "N")

    # Check if the peptide is capped or not
    if geo.residue_name == "ACE":
        CA = Atom("CH3", CA_coord, 0.0, 1.0, " ", " CH3", 0, "C")
    else:
        CA = Atom("CA", CA_coord, 0.0, 1.0, " ", " CA", 0, "C")

    C = Atom("C", C_coord, 0.0, 1.0, " ", " C", 0, "C")

    ##Create Carbonyl atom (to be moved later)
    C_O_length = geo.C_O_length
    CA_C_O_angle = geo.CA_C_O_angle
    N_CA_C_O_diangle = geo.N_CA_C_O_diangle

    carbonyl = calculateCoordinates(
        N, CA, C, C_O_length, CA_C_O_angle, N_CA_C_O_diangle
    )
    O = Atom("O", carbonyl, 0.0, 1.0, " ", " O", 0, "O")

    res = make_res_of_type(segID, N, CA, C, O, geo)

    cha = Chain("A")
    cha.add(res)

    mod = Model(0)
    mod.add(cha)

    struc = Structure("X")
    struc.add(mod)
    return struc


def getReferenceResidue(structure: Structure, index) -> Residue:
    """Returns the first (index = 0) or last (index = -1) residue of chain A model 0 of the given structure.

    This function is a helper function that should not normally be called
    directly."""

    # If the following line doesn't work we're in trouble.
    # Likely initialize_res() wasn't called.
    resRef = structure[0]["A"].child_list[index]
    name = resRef.get_resname()

    # If the residue is not an amino acid we're in trouble.
    # Likely somebody is trying to append residues to an existing
    # structure that has non-amino-acid molecules in the chain.
    if name in ["ACE", "NME"]:
        pass
    else:
        assert is_aa(resRef)

    return resRef


def add_residue_from_geo(structure: Structure, geo: Geo) -> Structure:
    """Adds a residue to chain A model 0 of the given structure, and
    returns the new structure. The residue to be added is determined by
    the geometry object given as second argument.

    This function is a helper function and should not normally be called
    directly. Call add_residue() instead."""
    resRef = getReferenceResidue(structure, -1)
    AA = geo.residue_name
    segID = resRef.get_id()[1]
    segID += 1

    ##geometry to bring together residue
    peptide_bond = geo.peptide_bond
    CA_C_N_angle = geo.CA_C_N_angle
    C_N_CA_angle = geo.C_N_CA_angle

    ##Backbone Coordinates
    N_CA_C_angle = geo.N_CA_C_angle
    CA_N_length = geo.CA_N_length
    CA_C_length = geo.CA_C_length
    phi = geo.phi
    psi_im1 = geo.psi_im1
    omega = geo.omega

    if resRef.get_resname() == "ACE":
        CA_name = "CH3"
    else:
        CA_name = "CA"

    N_coord = calculateCoordinates(
        resRef["N"], resRef[CA_name], resRef["C"], peptide_bond, CA_C_N_angle, psi_im1
    )
    N = Atom("N", N_coord, 0.0, 1.0, " ", " N", 0, "N")

    CA_coord = calculateCoordinates(
        resRef[CA_name], resRef["C"], N, CA_N_length, C_N_CA_angle, omega
    )
    CA = Atom("CA", CA_coord, 0.0, 1.0, " ", " CA", 0, "C")

    C_coord = calculateCoordinates(resRef["C"], N, CA, CA_C_length, N_CA_C_angle, phi)
    C = Atom("C", C_coord, 0.0, 1.0, " ", " C", 0, "C")

    ##Create Carbonyl atom (to be moved later)
    C_O_length = geo.C_O_length
    CA_C_O_angle = geo.CA_C_O_angle
    N_CA_C_O_diangle = geo.N_CA_C_O_diangle

    carbonyl = calculateCoordinates(
        N, CA, C, C_O_length, CA_C_O_angle, N_CA_C_O_diangle
    )
    O = Atom("O", carbonyl, 0.0, 1.0, " ", " O", 0, "O")

    if geo.residue_name == "NME":
        CA = Atom("CH3", CA_coord, 0.0, 1.0, " ", " CH3", 0, "C")
        new_CA_name = "CH3"
    else:
        new_CA_name = "CA"

    res = make_res_of_type(segID, N, CA, C, O, geo)

    resRef["O"].set_coord(
        calculateCoordinates(
            res["N"], resRef[CA_name], resRef["C"], C_O_length, CA_C_O_angle, 180.0
        )
    )

    ghost = Atom(
        "N",
        calculateCoordinates(
            res["N"], res[new_CA_name], res["C"], peptide_bond, CA_C_N_angle, psi_im1
        ),
        0.0,
        0.0,
        " ",
        "N",
        0,
        "N",
    )
    res["O"].set_coord(
        calculateCoordinates(
            res["N"], res[new_CA_name], res["C"], C_O_length, CA_C_O_angle, 180.0
        )
    )

    structure[0]["A"].add(res)

    if geo.residue_name == "NME":
        if structure[0]["A"][1].get_resname() == "ACE":
            del structure[0]["A"][1]["N"]
        del structure[0]["A"][segID]["C"]
        del structure[0]["A"][segID]["O"]

    return structure


def make_extended_structure(AA_chain: str, capping: bool = False) -> Structure:
    """Place a sequence of amino acids into a peptide in the extended
    conformation. The argument AA_chain holds the sequence of amino
    acids to be used, while capping can be set to True in order to
    cap the peptide with both ACE and NME residues."""
    if capping:
        geo = geometry("ACE")
        start = 0
    else:
        geo = geometry(AA_chain[0])
        start = 1

    struc = initialize_res(geo)

    for i in range(start, len(AA_chain)):
        AA = AA_chain[i]
        geo = geometry(AA)
        add_residue(struc, geo)

    if capping:
        geo = geometry("NME")
        add_residue(struc, geo)

    return struc


def add_residue(
    structure: Structure, residue: Union[Geo, str], phi=-120, psi_im1=140, omega=-370
) -> Structure:
    """Adds a residue to chain A model 0 of the given structure, and
    returns the new structure. The residue to be added can be specified
    in two ways: either as a geometry object (in which case
    the remaining arguments phi, psi_im1, and omega are ignored) or as a
    single-letter amino-acid code. In the latter case, the optional
    arguments phi, psi_im1, and omega specify the corresponding backbone
    angles.

    When omega is specified, it needs to be a value greater than or equal
    to -360. Values below -360 are ignored."""

    if isinstance(residue, Geo):
        geo = residue
    elif isinstance(residue, str):
        geo = geometry(residue)
        geo.phi = phi
        geo.psi_im1 = psi_im1
        if omega > -361:
            geo.omega = omega
    else:
        raise ValueError("Invalid residue argument:", residue)

    return add_residue_from_geo(structure, geo)


def make_structure(
    AA_chain: str, phi: List[float], psi_im1: List[float], omega: Optional[List] = None
) -> Structure:
    """Place a sequence of amino acids into a peptide with specified
    backbone dihedral angles. The argument AA_chain holds the
    sequence of amino acids to be used. The arguments phi and psi_im1 hold
    lists of backbone angles, one for each amino acid, *starting from
    the second amino acid in the chain*. The argument
    omega (optional) holds a list of omega angles, also starting from
    the second amino acid in the chain."""
    geo = geometry(AA_chain[0])
    struc = initialize_res(geo)

    if omega is None or not len(omega):
        for i in range(1, len(AA_chain)):
            AA = AA_chain[i]
            add_residue(struc, AA, phi[i - 1], psi_im1[i - 1])
    else:
        for i in range(1, len(AA_chain)):
            AA = AA_chain[i]
            add_residue(struc, AA, phi[i - 1], psi_im1[i - 1], omega[i - 1])

    return struc


def make_structure_from_geos(geos: List[Geo]) -> Structure:
    """Creates a structure out of a list of geometry objects."""
    model_structure = initialize_res(geos[0])
    for i in range(1, len(geos)):
        add_residue(model_structure, geos[i])

    return model_structure


def add_terminal_OXT(structure: Structure, C_OXT_length: float = 1.23) -> Structure:
    """Adds a terminal oxygen atom ('OXT') to the last residue of chain A model 0 of the given structure, and returns the new structure. The OXT atom object will be contained in the last residue object of the structure.

    This function should be used only when the structure object is completed and no further residues need to be appended."""

    rad = 180.0 / math.pi

    # obtain last residue infomation
    resRef = getReferenceResidue(structure, -1)
    N_resRef = resRef["N"]
    CA_resRef = resRef["CA"]
    C_resRef = resRef["C"]
    O_resRef = resRef["O"]

    n_vec = N_resRef.get_vector()
    ca_vec = CA_resRef.get_vector()
    c_vec = C_resRef.get_vector()
    o_vec = O_resRef.get_vector()

    # geometry to bring together residue
    CA_C_OXT_angle = calc_angle(ca_vec, c_vec, o_vec) * rad
    N_CA_C_O_diangle = calc_dihedral(n_vec, ca_vec, c_vec, o_vec) * rad
    N_CA_C_OXT_diangle = N_CA_C_O_diangle - 180.0
    if N_CA_C_O_diangle < 0:
        N_CA_C_OXT_diangle = N_CA_C_O_diangle + 180.0

    # OXT atom creation
    OXT_coord = calculateCoordinates(
        N_resRef, CA_resRef, C_resRef, C_OXT_length, CA_C_OXT_angle, N_CA_C_OXT_diangle
    )
    OXT = Atom("OXT", OXT_coord, 0.0, 1.0, " ", "OXT", 0, "O")

    # modify last residue of the structure to contain the OXT atom
    resRef.add(OXT)

    if structure[0]["A"][1].get_resname() == "ACE":
        del structure[0]["A"][1]["N"]

    return structure
