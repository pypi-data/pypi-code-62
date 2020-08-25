# -*- coding: utf-8 -*-
"""
Created on 2020-05-12

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict

class Xc:
   """
   xc class.
   
   Attributes
   ----------
   funcid : 1D array
      Functional id (LibXC).

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):

      if "names" in inpDict.keys() and not "funcid" in inpDict.keys():
         inpDict["funcid"] = [name2id(name.lower()) for name in inpDict["names"]]

      # required status
      reqDict = {
         "funcid": False,
      }
      # default values
      defDict = {
         "funcid": [1, 12],
      }    

      init_from_dict(self, reqDict, defDict, inpDict)

   def asdict(self):
      return utils_asdict(self)

def name2id(name):
   idDict = {
      'xc_lda_x' :                         1,  # Exchange                                                              */
      'xc_lda_c_wigner' :                  2,  # Wigner parametrization                                                */
      'xc_lda_c_rpa' :                     3,  # Random Phase Approximation                                            */
      'xc_lda_c_hl' :                      4,  # Hedin & Lundqvist                                                     */
      'xc_lda_c_gl' :                      5,  # Gunnarson & Lundqvist                                                 */
      'xc_lda_c_xalpha' :                  6,  # Slater Xalpha                                                         */
      'xc_lda_c_vwn' :                     7,  # Vosko, Wilk, & Nusair (5)                                             */
      'xc_lda_c_vwn_rpa' :                 8,  # Vosko, Wilk, & Nusair (RPA)                                           */
      'xc_lda_c_pz' :                      9,  # Perdew & Zunger                                                       */
      'xc_lda_c_pz_mod' :                 10,  # Perdew & Zunger (Modified)                                            */
      'xc_lda_c_ob_pz' :                  11,  # Ortiz & Ballone (PZ)                                                  */
      'xc_lda_c_pw' :                     12,  # Perdew & Wang                                                         */
      'xc_lda_c_pw_mod' :                 13,  # Perdew & Wang (Modified)                                              */
      'xc_lda_c_ob_pw' :                  14,  # Ortiz & Ballone (PW)                                                  */
      'xc_lda_c_2d_amgb' :                15,  # Attaccalite et al                                                     */
      'xc_lda_c_2d_prm' :                 16,  # Pittalis, Rasanen & Marques correlation in 2D                         */
      'xc_lda_c_vbh' :                    17,  # von Barth & Hedin                                                     */
      'xc_lda_c_1d_csc' :                 18,  # Casula, Sorella, and Senatore 1D correlation                          */
      'xc_lda_x_2d' :                     19,  # Exchange in 2D                                                        */
      'xc_lda_xc_teter93' :               20,  # Teter 93 parametrization                                              */
      'xc_lda_x_1d' :                     21,  # Exchange in 1D                                                        */
      'xc_lda_c_ml1' :                    22,  # Modified LSD (version 1) of Proynov and Salahub                       */
      'xc_lda_c_ml2' :                    23,  # Modified LSD (version 2) of Proynov and Salahub                       */
      'xc_lda_c_gombas' :                 24,  # Gombas parametrization                                                */
      'xc_lda_c_pw_rpa' :                 25,  # Perdew & Wang fit of the RPA                                          */
      'xc_lda_c_1d_loos' :                26,  # P-F Loos correlation LDA                                              */
      'xc_lda_c_rc04' :                   27,  # Ragot-Cortona                                                         */
      'xc_lda_c_vwn_1' :                  28,  # Vosko, Wilk, & Nusair (1)                                             */
      'xc_lda_c_vwn_2' :                  29,  # Vosko, Wilk, & Nusair (2)                                             */
      'xc_lda_c_vwn_3' :                  30,  # Vosko, Wilk, & Nusair (3)                                             */
      'xc_lda_c_vwn_4' :                  31,  # Vosko, Wilk, & Nusair (4)                                             */
      'xc_lda_xc_zlp' :                   43,  # Zhao, Levy & Parr, Eq. (20)                                           */
      'xc_lda_k_tf' :                     50,  # Thomas-Fermi kinetic energy functional                                */
      'xc_lda_k_lp' :                     51,  # Lee and Parr Gaussian ansatz                                          */
      'xc_lda_xc_ksdt' :                 259,  # Karasiev et al. parametrization                                       */
      'xc_lda_c_chachiyo' :              287,  # Chachiyo simple 2 parameter correlation                               */
      'xc_lda_c_lp96' :                  289,  # Liu-Parr correlation                                                  */
      'xc_lda_x_rel' :                   532,  # Relativistic exchange                                                 */
      'xc_lda_xc_1d_ehwlrg_1' :          536,  # LDA constructed from slab-like systems of 1 electron                  */
      'xc_lda_xc_1d_ehwlrg_2' :          537,  # LDA constructed from slab-like systems of 2 electrons                 */
      'xc_lda_xc_1d_ehwlrg_3' :          538,  # LDA constructed from slab-like systems of 3 electrons                 */
      'xc_lda_x_erf' :                   546,  # Attenuated exchange LDA (erf)                                         */
      'xc_lda_xc_lp_a' :                 547,  # Lee-Parr reparametrization B                                          */
      'xc_lda_xc_lp_b' :                 548,  # Lee-Parr reparametrization B                                          */
      'xc_lda_x_rae' :                   549,  # Rae self-energy corrected exchange                                    */
      'xc_lda_k_zlp' :                   550,  # kinetic energy version of ZLP                                         */
      'xc_lda_c_mcweeny' :               551,  # McWeeny 76                                                            */
      'xc_lda_c_br78' :                  552,  # Brual & Rothstein 78                                                  */
      'xc_lda_c_pk09' :                  554,  # Proynov and Kong 2009                                                 */
      'xc_lda_c_ow_lyp' :                573,  # Wigner with corresponding LYP parameters                              */
      'xc_lda_c_ow' :                    574,  # Optimized Wigner                                                      */
      'xc_lda_xc_gdsmfb' :               577,  # Groth et al. parametrization                                          */
      'xc_lda_c_gk72' :                  578,  # Gordon and Kim 1972                                                   */
      'xc_lda_c_karasiev' :              579,  # Karasiev reparameterization of Chachiyo                               */
      'xc_lda_k_lp96' :                  580,  # Liu-Parr kinetic                                                      */
      'xc_gga_x_gam' :                    32,  # GAM functional from Minnesota                                         */
      'xc_gga_c_gam' :                    33,  # GAM functional from Minnesota                                         */
      'xc_gga_x_hcth_a' :                 34,  # HCTH-A                                                                */
      'xc_gga_x_ev93' :                   35,  # Engel and Vosko                                                       */
      'xc_gga_x_bcgp' :                   38,  # Burke, Cancio, Gould, and Pittalis                                    */
      'xc_gga_c_bcgp' :                   39,  # Burke, Cancio, Gould, and Pittalis                                    */
      'xc_gga_x_lambda_oc2_n' :           40,  # lambda_OC2(N) version of PBE                                          */
      'xc_gga_x_b86_r' :                  41,  # Revised Becke 86 Xalpha,beta,gamma (with mod. grad. correction)       */
      'xc_gga_x_lambda_ch_n' :            44,  # lambda_CH(N) version of PBE                                           */
      'xc_gga_x_lambda_lo_n' :            45,  # lambda_LO(N) version of PBE                                           */
      'xc_gga_x_hjs_b88_v2' :             46,  # HJS screened exchange corrected B88 version                           */
      'xc_gga_c_q2d' :                    47,  # Chiodo et al                                                          */
      'xc_gga_x_q2d' :                    48,  # Chiodo et al                                                          */
      'xc_gga_x_pbe_mol' :                49,  # Del Campo, Gazquez, Trickey and Vela (PBE-like)                       */
      'xc_gga_k_tfvw' :                   52,  # Thomas-Fermi plus von Weiszaecker correction                          */
      'xc_gga_k_revapbeint' :             53,  # interpolated version of REVAPBE                                       */
      'xc_gga_k_apbeint' :                54,  # interpolated version of APBE                                          */
      'xc_gga_k_revapbe' :                55,  # revised APBE                                                          */
      'xc_gga_x_ak13' :                   56,  # Armiento & Kuemmel 2013                                               */
      'xc_gga_k_meyer' :                  57,  # Meyer,  Wang, and Young                                               */
      'xc_gga_x_lv_rpw86' :               58,  # Berland and Hyldgaard                                                 */
      'xc_gga_x_pbe_tca' :                59,  # PBE revised by Tognetti et al                                         */
      'xc_gga_x_pbeint' :                 60,  # PBE for hybrid interfaces                                             */
      'xc_gga_c_zpbeint' :                61,  # spin-dependent gradient correction to PBEint                          */
      'xc_gga_c_pbeint' :                 62,  # PBE for hybrid interfaces                                             */
      'xc_gga_c_zpbesol' :                63,  # spin-dependent gradient correction to PBEsol                          */
      'xc_gga_xc_opbe_d' :                65,  # oPBE_D functional of Goerigk and Grimme                               */
      'xc_gga_xc_opwlyp_d' :              66,  # oPWLYP-D functional of Goerigk and Grimme                             */
      'xc_gga_xc_oblyp_d' :               67,  # oBLYP-D functional of Goerigk and Grimme                              */
      'xc_gga_x_vmt84_ge' :               68,  # VMT{8,4} with constraint satisfaction with mu = mu_GE                 */
      'xc_gga_x_vmt84_pbe' :              69,  # VMT{8,4} with constraint satisfaction with mu = mu_PBE                */
      'xc_gga_x_vmt_ge' :                 70,  # Vela, Medel, and Trickey with mu = mu_GE                              */
      'xc_gga_x_vmt_pbe' :                71,  # Vela, Medel, and Trickey with mu = mu_PBE                             */
      'xc_gga_c_n12_sx' :                 79,  # N12-SX functional from Minnesota                                      */
      'xc_gga_c_n12' :                    80,  # N12 functional from Minnesota                                         */
      'xc_gga_x_n12' :                    82,  # N12 functional from Minnesota                                         */
      'xc_gga_c_regtpss' :                83,  # Regularized TPSS correlation (ex-VPBE)                                */
      'xc_gga_c_op_xalpha' :              84,  # one-parameter progressive functional (XALPHA version)                 */
      'xc_gga_c_op_g96' :                 85,  # one-parameter progressive functional (G96 version)                    */
      'xc_gga_c_op_pbe' :                 86,  # one-parameter progressive functional (PBE version)                    */
      'xc_gga_c_op_b88' :                 87,  # one-parameter progressive functional (B88 version)                    */
      'xc_gga_c_ft97' :                   88,  # Filatov & Thiel correlation                                           */
      'xc_gga_c_spbe' :                   89,  # PBE correlation to be used with the SSB exchange                      */
      'xc_gga_x_ssb_sw' :                 90,  # Swart, Sola and Bickelhaupt correction to PBE                         */
      'xc_gga_x_ssb' :                    91,  # Swart, Sola and Bickelhaupt                                           */
      'xc_gga_x_ssb_d' :                  92,  # Swart, Sola and Bickelhaupt dispersion                                */
      'xc_gga_xc_hcth_407p' :             93,  # HCTH/407+                                                             */
      'xc_gga_xc_hcth_p76' :              94,  # HCTH p=7/6                                                            */
      'xc_gga_xc_hcth_p14' :              95,  # HCTH p=1/4                                                            */
      'xc_gga_xc_b97_gga1' :              96,  # Becke 97 GGA-1                                                        */
      'xc_gga_c_hcth_a' :                 97,  # HCTH-A                                                                */
      'xc_gga_x_bpccac' :                 98,  # BPCCAC (GRAC for the energy)                                          */
      'xc_gga_c_revtca' :                 99,  # Tognetti, Cortona, Adamo (revised)                                    */
      'xc_gga_c_tca' :                   100,  # Tognetti, Cortona, Adamo                                              */
      'xc_gga_x_pbe' :                   101,  # Perdew, Burke & Ernzerhof exchange                                    */
      'xc_gga_x_pbe_r' :                 102,  # Perdew, Burke & Ernzerhof exchange (revised)                          */
      'xc_gga_x_b86' :                   103,  # Becke 86 Xalpha,beta,gamma                                            */
      'xc_gga_x_herman' :                104,  # Herman et al original GGA                                             */
      'xc_gga_x_b86_mgc' :               105,  # Becke 86 Xalpha,beta,gamma (with mod. grad. correction)               */
      'xc_gga_x_b88' :                   106,  # Becke 88                                                              */
      'xc_gga_x_g96' :                   107,  # Gill 96                                                               */
      'xc_gga_x_pw86' :                  108,  # Perdew & Wang 86                                                      */
      'xc_gga_x_pw91' :                  109,  # Perdew & Wang 91                                                      */
      'xc_gga_x_optx' :                  110,  # Handy & Cohen OPTX 01                                                 */
      'xc_gga_x_dk87_r1' :               111,  # dePristo & Kress 87 (version R1)                                      */
      'xc_gga_x_dk87_r2' :               112,  # dePristo & Kress 87 (version R2)                                      */
      'xc_gga_x_lg93' :                  113,  # Lacks & Gordon 93                                                     */
      'xc_gga_x_ft97_a' :                114,  # Filatov & Thiel 97 (version A)                                        */
      'xc_gga_x_ft97_b' :                115,  # Filatov & Thiel 97 (version B)                                        */
      'xc_gga_x_pbe_sol' :               116,  # Perdew, Burke & Ernzerhof exchange (solids)                           */
      'xc_gga_x_rpbe' :                  117,  # Hammer, Hansen & Norskov (PBE-like)                                   */
      'xc_gga_x_wc' :                    118,  # Wu & Cohen                                                            */
      'xc_gga_x_mpw91' :                 119,  # Modified form of PW91 by Adamo & Barone                               */
      'xc_gga_x_am05' :                  120,  # Armiento & Mattsson 05 exchange                                       */
      'xc_gga_x_pbea' :                  121,  # Madsen (PBE-like)                                                     */
      'xc_gga_x_mpbe' :                  122,  # Adamo & Barone modification to PBE                                    */
      'xc_gga_x_xpbe' :                  123,  # xPBE reparametrization by Xu & Goddard                                */
      'xc_gga_x_2d_b86_mgc' :            124,  # Becke 86 MGC for 2D systems                                           */
      'xc_gga_x_bayesian' :              125,  # Bayesian best fit for the enhancement factor                          */
      'xc_gga_x_pbe_jsjr' :              126,  # JSJR reparametrization by Pedroza, Silva & Capelle                    */
      'xc_gga_x_2d_b88' :                127,  # Becke 88 in 2D                                                        */
      'xc_gga_x_2d_b86' :                128,  # Becke 86 Xalpha,beta,gamma                                            */
      'xc_gga_x_2d_pbe' :                129,  # Perdew, Burke & Ernzerhof exchange in 2D                              */
      'xc_gga_c_pbe' :                   130,  # Perdew, Burke & Ernzerhof correlation                                 */
      'xc_gga_c_lyp' :                   131,  # Lee, Yang & Parr                                                      */
      'xc_gga_c_p86' :                   132,  # Perdew 86                                                             */
      'xc_gga_c_pbe_sol' :               133,  # Perdew, Burke & Ernzerhof correlation SOL                             */
      'xc_gga_c_pw91' :                  134,  # Perdew & Wang 91                                                      */
      'xc_gga_c_am05' :                  135,  # Armiento & Mattsson 05 correlation                                    */
      'xc_gga_c_xpbe' :                  136,  # xPBE reparametrization by Xu & Goddard                                */
      'xc_gga_c_lm' :                    137,  # Langreth and Mehl correlation                                         */
      'xc_gga_c_pbe_jrgx' :              138,  # JRGX reparametrization by Pedroza, Silva & Capelle                    */
      'xc_gga_x_optb88_vdw' :            139,  # Becke 88 reoptimized to be used with vdW functional of Dion et al     */
      'xc_gga_x_pbek1_vdw' :             140,  # PBE reparametrization for vdW                                         */
      'xc_gga_x_optpbe_vdw' :            141,  # PBE reparametrization for vdW                                         */
      'xc_gga_x_rge2' :                  142,  # Regularized PBE                                                       */
      'xc_gga_c_rge2' :                  143,  # Regularized PBE                                                       */
      'xc_gga_x_rpw86' :                 144,  # refitted Perdew & Wang 86                                             */
      'xc_gga_x_kt1' :                   145,  # Exchange part of Keal and Tozer version 1                             */
      'xc_gga_xc_kt2' :                  146,  # Keal and Tozer version 2                                              */
      'xc_gga_c_wl' :                    147,  # Wilson & Levy                                                         */
      'xc_gga_c_wi' :                    148,  # Wilson & Ivanov                                                       */
      'xc_gga_x_mb88' :                  149,  # Modified Becke 88 for proton transfer                                 */
      'xc_gga_x_sogga' :                 150,  # Second-order generalized gradient approximation                       */
      'xc_gga_x_sogga11' :               151,  # Second-order generalized gradient approximation 2011                  */
      'xc_gga_c_sogga11' :               152,  # Second-order generalized gradient approximation 2011                  */
      'xc_gga_c_wi0' :                   153,  # Wilson & Ivanov initial version                                       */
      'xc_gga_xc_th1' :                  154,  # Tozer and Handy v. 1                                                  */
      'xc_gga_xc_th2' :                  155,  # Tozer and Handy v. 2                                                  */
      'xc_gga_xc_th3' :                  156,  # Tozer and Handy v. 3                                                  */
      'xc_gga_xc_th4' :                  157,  # Tozer and Handy v. 4                                                  */
      'xc_gga_x_c09x' :                  158,  # C09x to be used with the VdW of Rutgers-Chalmers                      */
      'xc_gga_c_sogga11_x' :             159,  # To be used with HYB_GGA_X_SOGGA11_X                                   */
      'xc_gga_x_lb' :                    160,  # van Leeuwen & Baerends                                                */
      'xc_gga_xc_hcth_93' :              161,  # HCTH functional fitted to  93 molecules                               */
      'xc_gga_xc_hcth_120' :             162,  # HCTH functional fitted to 120 molecules                               */
      'xc_gga_xc_hcth_147' :             163,  # HCTH functional fitted to 147 molecules                               */
      'xc_gga_xc_hcth_407' :             164,  # HCTH functional fitted to 407 molecules                               */
      'xc_gga_xc_edf1' :                 165,  # Empirical functionals from Adamson, Gill, and Pople                   */
      'xc_gga_xc_xlyp' :                 166,  # XLYP functional                                                       */
      'xc_gga_xc_kt1' :                  167,  # Keal and Tozer version 1                                              */
      'xc_gga_xc_b97_d' :                170,  # Grimme functional to be used with C6 vdW term                         */
      'xc_gga_xc_pbe1w' :                173,  # Functionals fitted for water                                          */
      'xc_gga_xc_mpwlyp1w' :             174,  # Functionals fitted for water                                          */
      'xc_gga_xc_pbelyp1w' :             175,  # Functionals fitted for water                                          */
      'xc_gga_x_lbm' :                   182,  # van Leeuwen & Baerends modified                                       */
      'xc_gga_x_ol2' :                   183,  # Exchange form based on Ou-Yang and Levy v.2                           */
      'xc_gga_x_apbe' :                  184,  # mu fixed from the semiclassical neutral atom                          */
      'xc_gga_k_apbe' :                  185,  # mu fixed from the semiclassical neutral atom                          */
      'xc_gga_c_apbe' :                  186,  # mu fixed from the semiclassical neutral atom                          */
      'xc_gga_k_tw1' :                   187,  # Tran and Wesolowski set 1 (Table II)                                  */
      'xc_gga_k_tw2' :                   188,  # Tran and Wesolowski set 2 (Table II)                                  */
      'xc_gga_k_tw3' :                   189,  # Tran and Wesolowski set 3 (Table II)                                  */
      'xc_gga_k_tw4' :                   190,  # Tran and Wesolowski set 4 (Table II)                                  */
      'xc_gga_x_htbs' :                  191,  # Haas, Tran, Blaha, and Schwarz                                        */
      'xc_gga_x_airy' :                  192,  # Constantin et al based on the Airy gas                                */
      'xc_gga_x_lag' :                   193,  # Local Airy Gas                                                        */
      'xc_gga_xc_mohlyp' :               194,  # Functional for organometallic chemistry                               */
      'xc_gga_xc_mohlyp2' :              195,  # Functional for barrier heights                                        */
      'xc_gga_xc_th_fl' :                196,  # Tozer and Handy v. FL                                                 */
      'xc_gga_xc_th_fc' :                197,  # Tozer and Handy v. FC                                                 */
      'xc_gga_xc_th_fcfo' :              198,  # Tozer and Handy v. FCFO                                               */
      'xc_gga_xc_th_fco' :               199,  # Tozer and Handy v. FCO                                                */
      'xc_gga_c_optc' :                  200,  # Optimized correlation functional of Cohen and Handy                   */
      'xc_gga_c_pbeloc' :                246,  # Semilocal dynamical correlation                                       */
      'xc_gga_xc_vv10' :                 255,  # Vydrov and Van Voorhis                                                */
      'xc_gga_c_pbefe' :                 258,  # PBE for formation energies                                            */
      'xc_gga_c_op_pw91' :               262,  # one-parameter progressive functional (PW91 version)                   */
      'xc_gga_x_pbefe' :                 265,  # PBE for formation energies                                            */
      'xc_gga_x_cap' :                   270,  # Correct Asymptotic Potential                                          */
      'xc_gga_x_eb88' :                  271,  # Non-empirical (excogitated) B88 functional of Becke and Elliott       */
      'xc_gga_c_pbe_mol' :               272,  # Del Campo, Gazquez, Trickey and Vela (PBE-like)                       */
      'xc_gga_k_absp3' :                 277,  # gamma-TFvW form by Acharya et al [g = 1 - 1.513/N^0.35]               */
      'xc_gga_k_absp4' :                 278,  # gamma-TFvW form by Acharya et al [g = l = 1/(1 + 1.332/N^(1/3))]      */
      'xc_gga_c_bmk' :                   280,  # Boese-Martin for kinetics                                             */
      'xc_gga_c_tau_hcth' :              281,  # correlation part of tau-hcth                                          */
      'xc_gga_c_hyb_tau_hcth' :          283,  # correlation part of hyb_tau-hcth                                      */
      'xc_gga_x_beefvdw' :               285,  # BEEF-vdW exchange                                                     */
      'xc_gga_xc_beefvdw' :              286,  # BEEF-vdW exchange-correlation                                         */
      'xc_gga_x_pbetrans' :              291,  # Gradient-based interpolation between PBE and revPBE                   */
      'xc_gga_x_chachiyo' :              298,  # Chachiyo exchange                                                     */
      'xc_gga_k_vw' :                    500,  # von Weiszaecker functional                                            */
      'xc_gga_k_ge2' :                   501,  # Second-order gradient expansion (l = 1/9)                             */
      'xc_gga_k_golden' :                502,  # TF-lambda-vW form by Golden (l = 13/45)                               */
      'xc_gga_k_yt65' :                  503,  # TF-lambda-vW form by Yonei and Tomishima (l = 1/5)                    */
      'xc_gga_k_baltin' :                504,  # TF-lambda-vW form by Baltin (l = 5/9)                                 */
      'xc_gga_k_lieb' :                  505,  # TF-lambda-vW form by Lieb (l = 0.185909191)                           */
      'xc_gga_k_absp1' :                 506,  # gamma-TFvW form by Acharya et al [g = 1 - 1.412/N^(1/3)]              */
      'xc_gga_k_absp2' :                 507,  # gamma-TFvW form by Acharya et al [g = 1 - 1.332/N^(1/3)]              */
      'xc_gga_k_gr' :                    508,  # gamma-TFvW form by Gazquez and Robles                                 */
      'xc_gga_k_ludena' :                509,  # gamma-TFvW form by Ludena                                             */
      'xc_gga_k_gp85' :                  510,  # gamma-TFvW form by Ghosh and Parr                                     */
      'xc_gga_k_pearson' :               511,  # Pearson                                                               */
      'xc_gga_k_ol1' :                   512,  # Ou-Yang and Levy v.1                                                  */
      'xc_gga_k_ol2' :                   513,  # Ou-Yang and Levy v.2                                                  */
      'xc_gga_k_fr_b88' :                514,  # Fuentealba & Reyes (B88 version)                                      */
      'xc_gga_k_fr_pw86' :               515,  # Fuentealba & Reyes (PW86 version)                                     */
      'xc_gga_k_dk' :                    516,  # DePristo and Kress                                                    */
      'xc_gga_k_perdew' :                517,  # Perdew                                                                */
      'xc_gga_k_vsk' :                   518,  # Vitos, Skriver, and Kollar                                            */
      'xc_gga_k_vjks' :                  519,  # Vitos, Johansson, Kollar, and Skriver                                 */
      'xc_gga_k_ernzerhof' :             520,  # Ernzerhof                                                             */
      'xc_gga_k_lc94' :                  521,  # Lembarki & Chermette                                                  */
      'xc_gga_k_llp' :                   522,  # Lee, Lee & Parr                                                       */
      'xc_gga_k_thakkar' :               523,  # Thakkar 1992                                                          */
      'xc_gga_x_wpbeh' :                 524,  # short-range version of the PBE                                        */
      'xc_gga_x_hjs_pbe' :               525,  # HJS screened exchange PBE version                                     */
      'xc_gga_x_hjs_pbe_sol' :           526,  # HJS screened exchange PBE_SOL version                                 */
      'xc_gga_x_hjs_b88' :               527,  # HJS screened exchange B88 version                                     */
      'xc_gga_x_hjs_b97x' :              528,  # HJS screened exchange B97x version                                    */
      'xc_gga_x_ityh' :                  529,  # short-range recipe for exchange GGA functionals                       */
      'xc_gga_x_sfat' :                  530,  # short-range recipe for exchange GGA functionals                       */
      'xc_gga_x_sg4' :                   533,  # Semiclassical GGA at fourth order                                     */
      'xc_gga_c_sg4' :                   534,  # Semiclassical GGA at fourth order                                     */
      'xc_gga_x_gg99' :                  535,  # Gilbert and Gill 1999                                                 */
      'xc_gga_x_pbepow' :                539,  # PBE power                                                             */
      'xc_gga_x_kgg99' :                 544,  # Gilbert and Gill 1999 (mixed)                                         */
      'xc_gga_xc_hle16' :                545,  # high local exchange 2016                                              */
      'xc_gga_c_scan_e0' :               553,  # GGA component of SCAN                                                 */
      'xc_gga_c_gapc' :                  555,  # GapC                                                                  */
      'xc_gga_c_gaploc' :                556,  # Gaploc                                                                */
      'xc_gga_c_zvpbeint' :              557,  # another spin-dependent correction to PBEint                           */
      'xc_gga_c_zvpbesol' :              558,  # another spin-dependent correction to PBEsol                           */
      'xc_gga_c_tm_lyp' :                559,  # Takkar and McCarthy reparametrization                                 */
      'xc_gga_c_tm_pbe' :                560,  # Thakkar and McCarthy reparametrization                                */
      'xc_gga_c_w94' :                   561,  # Wilson 94 (Eq. 25)                                                    */
      'xc_gga_c_cs1' :                   565,  # A dynamical correlation functional                                    */
      'xc_gga_x_b88m' :                  570,  # Becke 88 reoptimized to be used with mgga_c_tau1                      */
      'xc_gga_k_pbe3' :                  595,  # Three parameter PBE-like expansion                                    */
      'xc_gga_k_pbe4' :                  596,  # Four  parameter PBE-like expansion                                    */
      'xc_gga_k_exp4' :                  597,  # Intermediate form between PBE3 and PBE4                               */
      'xc_hyb_gga_x_n12_sx' :             81,  # N12-SX functional from Minnesota                                      */
      'xc_hyb_gga_xc_b97_1p' :           266,  # version of B97 by Cohen and Handy                                     */
      'xc_hyb_gga_xc_pbe_mol0' :         273,  # PBEmol0                                                               */
      'xc_hyb_gga_xc_pbe_sol0' :         274,  # PBEsol0                                                               */
      'xc_hyb_gga_xc_pbeb0' :            275,  # PBEbeta0                                                              */
      'xc_hyb_gga_xc_pbe_molb0' :        276,  # PBEmolbeta0                                                           */
      'xc_hyb_gga_xc_pbe50' :            290,  # PBE0 with 50% exx                                                     */
      'xc_hyb_gga_xc_b3pw91' :           401,  # The original (ACM) hybrid of Becke                                    */
      'xc_hyb_gga_xc_b3lyp' :            402,  # The (in)famous B3LYP                                                  */
      'xc_hyb_gga_xc_b3p86' :            403,  # Perdew 86 hybrid similar to B3PW91                                    */
      'xc_hyb_gga_xc_o3lyp' :            404,  # hybrid using the optx functional                                      */
      'xc_hyb_gga_xc_mpw1k' :            405,  # mixture of mPW91 and PW91 optimized for kinetics                      */
      'xc_hyb_gga_xc_pbeh' :             406,  # aka PBE0 or PBE1PBE                                                   */
      'xc_hyb_gga_xc_b97' :              407,  # Becke 97                                                              */
      'xc_hyb_gga_xc_b97_1' :            408,  # Becke 97-1                                                            */
      'xc_hyb_gga_xc_b97_2' :            410,  # Becke 97-2                                                            */
      'xc_hyb_gga_xc_x3lyp' :            411,  # hybrid by Xu and Goddard                                              */
      'xc_hyb_gga_xc_b1wc' :             412,  # Becke 1-parameter mixture of WC and PBE                               */
      'xc_hyb_gga_xc_b97_k' :            413,  # Boese-Martin for Kinetics                                             */
      'xc_hyb_gga_xc_b97_3' :            414,  # Becke 97-3                                                            */
      'xc_hyb_gga_xc_mpw3pw' :           415,  # mixture with the mPW functional                                       */
      'xc_hyb_gga_xc_b1lyp' :            416,  # Becke 1-parameter mixture of B88 and LYP                              */
      'xc_hyb_gga_xc_b1pw91' :           417,  # Becke 1-parameter mixture of B88 and PW91                             */
      'xc_hyb_gga_xc_mpw1pw' :           418,  # Becke 1-parameter mixture of mPW91 and PW91                           */
      'xc_hyb_gga_xc_mpw3lyp' :          419,  # mixture of mPW and LYP                                                */
      'xc_hyb_gga_xc_sb98_1a' :          420,  # Schmider-Becke 98 parameterization 1a                                 */
      'xc_hyb_gga_xc_sb98_1b' :          421,  # Schmider-Becke 98 parameterization 1b                                 */
      'xc_hyb_gga_xc_sb98_1c' :          422,  # Schmider-Becke 98 parameterization 1c                                 */
      'xc_hyb_gga_xc_sb98_2a' :          423,  # Schmider-Becke 98 parameterization 2a                                 */
      'xc_hyb_gga_xc_sb98_2b' :          424,  # Schmider-Becke 98 parameterization 2b                                 */
      'xc_hyb_gga_xc_sb98_2c' :          425,  # Schmider-Becke 98 parameterization 2c                                 */
      'xc_hyb_gga_x_sogga11_x' :         426,  # Hybrid based on SOGGA11 form                                          */
      'xc_hyb_gga_xc_hse03' :            427,  # the 2003 version of the screened hybrid HSE                           */
      'xc_hyb_gga_xc_hse06' :            428,  # the 2006 version of the screened hybrid HSE                           */
      'xc_hyb_gga_xc_hjs_pbe' :          429,  # HJS hybrid screened exchange PBE version                              */
      'xc_hyb_gga_xc_hjs_pbe_sol' :      430,  # HJS hybrid screened exchange PBE_SOL version                          */
      'xc_hyb_gga_xc_hjs_b88' :          431,  # HJS hybrid screened exchange B88 version                              */
      'xc_hyb_gga_xc_hjs_b97x' :         432,  # HJS hybrid screened exchange B97x version                             */
      'xc_hyb_gga_xc_cam_b3lyp' :        433,  # CAM version of B3LYP                                                  */
      'xc_hyb_gga_xc_tuned_cam_b3lyp' :  434,  # CAM version of B3LYP tuned for excitations                            */
      'xc_hyb_gga_xc_bhandh' :           435,  # Becke half-and-half                                                   */
      'xc_hyb_gga_xc_bhandhlyp' :        436,  # Becke half-and-half with B88 exchange                                 */
      'xc_hyb_gga_xc_mb3lyp_rc04' :      437,  # B3LYP with RC04 LDA                                                   */
      'xc_hyb_gga_xc_mpwlyp1m' :         453,  # MPW with 1 par. for metals/LYP                                        */
      'xc_hyb_gga_xc_revb3lyp' :         454,  # Revised B3LYP                                                         */
      'xc_hyb_gga_xc_camy_blyp' :        455,  # BLYP with yukawa screening                                            */
      'xc_hyb_gga_xc_pbe0_13' :          456,  # PBE0-1/3                                                              */
      'xc_hyb_gga_xc_b3lyps' :           459,  # B3LYP* functional                                                     */
      'xc_hyb_gga_xc_wb97' :             463,  # Chai and Head-Gordon                                                  */
      'xc_hyb_gga_xc_wb97x' :            464,  # Chai and Head-Gordon                                                  */
      'xc_hyb_gga_xc_lrc_wpbeh' :        465,  # Long-range corrected functional by Rorhdanz et al                     */
      'xc_hyb_gga_xc_wb97x_v' :          466,  # Mardirossian and Head-Gordon                                          */
      'xc_hyb_gga_xc_lcy_pbe' :          467,  # PBE with yukawa screening                                             */
      'xc_hyb_gga_xc_lcy_blyp' :         468,  # BLYP with yukawa screening                                            */
      'xc_hyb_gga_xc_lc_vv10' :          469,  # Vydrov and Van Voorhis                                                */
      'xc_hyb_gga_xc_camy_b3lyp' :       470,  # B3LYP with Yukawa screening                                           */
      'xc_hyb_gga_xc_wb97x_d' :          471,  # Chai and Head-Gordon                                                  */
      'xc_hyb_gga_xc_hpbeint' :          472,  # hPBEint                                                               */
      'xc_hyb_gga_xc_lrc_wpbe' :         473,  # Long-range corrected functional by Rorhdanz et al                     */
      'xc_hyb_gga_xc_b3lyp5' :           475,  # B3LYP with VWN functional 5 instead of RPA                            */
      'xc_hyb_gga_xc_edf2' :             476,  # Empirical functional from Lin, George and Gill                        */
      'xc_hyb_gga_xc_cap0' :             477,  # Correct Asymptotic Potential hybrid                                   */
      'xc_hyb_gga_xc_lc_wpbe' :          478,  # Long-range corrected functional by Vydrov and Scuseria                */
      'xc_hyb_gga_xc_hse12' :            479,  # HSE12 by Moussa, Schultz and Chelikowsky                              */
      'xc_hyb_gga_xc_hse12s' :           480,  # Short-range HSE12 by Moussa, Schultz, and Chelikowsky                 */
      'xc_hyb_gga_xc_hse_sol' :          481,  # HSEsol functional by Schimka, Harl, and Kresse                        */
      'xc_hyb_gga_xc_cam_qtp_01' :       482,  # CAM-QTP(01): CAM-B3LYP retuned using ionization potentials of water   */
      'xc_hyb_gga_xc_mpw1lyp' :          483,  # Becke 1-parameter mixture of mPW91 and LYP                            */
      'xc_hyb_gga_xc_mpw1pbe' :          484,  # Becke 1-parameter mixture of mPW91 and PBE                            */
      'xc_hyb_gga_xc_kmlyp' :            485,  # Kang-Musgrave hybrid                                                  */
      'xc_hyb_gga_xc_b5050lyp' :         572,  # Like B3LYP but more exact exchange                                    */
      'xc_mgga_c_dldf' :                  37,  # Dispersionless Density Functional                                     */
      'xc_mgga_xc_zlp' :                  42,  # Zhao, Levy & Parr, Eq. (21)                                           */
      'xc_mgga_xc_otpss_d' :              64,  # oTPSS_D functional of Goerigk and Grimme                              */
      'xc_mgga_c_cs' :                    72,  # Colle and Salvetti                                                    */
      'xc_mgga_c_mn12_sx' :               73,  # MN12-SX correlation functional from Minnesota                         */
      'xc_mgga_c_mn12_l' :                74,  # MN12-L correlation functional from Minnesota                          */
      'xc_mgga_c_m11_l' :                 75,  # M11-L correlation functional from Minnesota                           */
      'xc_mgga_c_m11' :                   76,  # M11 correlation functional from Minnesota                             */
      'xc_mgga_c_m08_so' :                77,  # M08-SO correlation functional from Minnesota                          */
      'xc_mgga_c_m08_hx' :                78,  # M08-HX correlation functional from Minnesota                          */
      'xc_mgga_x_lta' :                  201,  # Local tau approximation of Ernzerhof & Scuseria                       */
      'xc_mgga_x_tpss' :                 202,  # Tao, Perdew, Staroverov & Scuseria exchange                           */
      'xc_mgga_x_m06_l' :                203,  # M06-L exchange functional from Minnesota                              */
      'xc_mgga_x_gvt4' :                 204,  # GVT4 from Van Voorhis and Scuseria                                    */
      'xc_mgga_x_tau_hcth' :             205,  # tau-HCTH from Boese and Handy                                         */
      'xc_mgga_x_br89' :                 206,  # Becke-Roussel 89                                                      */
      'xc_mgga_x_bj06' :                 207,  # Becke & Johnson correction to Becke-Roussel 89                        */
      'xc_mgga_x_tb09' :                 208,  # Tran & Blaha correction to Becke & Johnson                            */
      'xc_mgga_x_rpp09' :                209,  # Rasanen, Pittalis, and Proetto correction to Becke & Johnson          */
      'xc_mgga_x_2d_prhg07' :            210,  # Pittalis, Rasanen, Helbig, Gross Exchange Functional                  */
      'xc_mgga_x_2d_prhg07_prp10' :      211,  # PRGH07 with PRP10 correction                                          */
      'xc_mgga_x_revtpss' :              212,  # revised Tao, Perdew, Staroverov & Scuseria exchange                   */
      'xc_mgga_x_pkzb' :                 213,  # Perdew, Kurth, Zupan, and Blaha                                       */
      'xc_mgga_x_ms0' :                  221,  # MS exchange of Sun, Xiao, and Ruzsinszky                              */
      'xc_mgga_x_ms1' :                  222,  # MS1 exchange of Sun, et al                                            */
      'xc_mgga_x_ms2' :                  223,  # MS2 exchange of Sun, et al                                            */
      'xc_mgga_x_m11_l' :                226,  # M11-L exchange functional from Minnesota                              */
      'xc_mgga_x_mn12_l' :               227,  # MN12-L exchange functional from Minnesota                             */
      'xc_mgga_xc_cc06' :                229,  # Cancio and Chou 2006                                                  */
      'xc_mgga_x_mk00' :                 230,  # Exchange for accurate virtual orbital energies                        */
      'xc_mgga_c_tpss' :                 231,  # Tao, Perdew, Staroverov & Scuseria correlation                        */
      'xc_mgga_c_vsxc' :                 232,  # VSxc from Van Voorhis and Scuseria (correlation part)                 */
      'xc_mgga_c_m06_l' :                233,  # M06-L correlation functional from Minnesota                           */
      'xc_mgga_c_m06_hf' :               234,  # M06-HF correlation functional from Minnesota                          */
      'xc_mgga_c_m06' :                  235,  # M06 correlation functional from Minnesota                             */
      'xc_mgga_c_m06_2x' :               236,  # M06-2X correlation functional from Minnesota                          */
      'xc_mgga_c_m05' :                  237,  # M05 correlation functional from Minnesota                             */
      'xc_mgga_c_m05_2x' :               238,  # M05-2X correlation functional from Minnesota                          */
      'xc_mgga_c_pkzb' :                 239,  # Perdew, Kurth, Zupan, and Blaha                                       */
      'xc_mgga_c_bc95' :                 240,  # Becke correlation 95                                                  */
      'xc_mgga_c_revtpss' :              241,  # revised TPSS correlation                                              */
      'xc_mgga_xc_tpsslyp1w' :           242,  # Functionals fitted for water                                          */
      'xc_mgga_x_mk00b' :                243,  # Exchange for accurate virtual orbital energies (v. B)                 */
      'xc_mgga_x_bloc' :                 244,  # functional with balanced localization                                 */
      'xc_mgga_x_modtpss' :              245,  # Modified Tao, Perdew, Staroverov & Scuseria exchange                  */
      'xc_mgga_c_tpssloc' :              247,  # Semilocal dynamical correlation                                       */
      'xc_mgga_x_mbeef' :                249,  # mBEEF exchange                                                        */
      'xc_mgga_x_mbeefvdw' :             250,  # mBEEF-vdW exchange                                                    */
      'xc_mgga_xc_b97m_v' :              254,  # Mardirossian and Head-Gordon                                          */
      'xc_mgga_x_mvs' :                  257,  # MVS exchange of Sun, Perdew, and Ruzsinszky                           */
      'xc_mgga_x_mn15_l' :               260,  # MN15-L exhange functional from Minnesota                              */
      'xc_mgga_c_mn15_l' :               261,  # MN15-L correlation functional from Minnesota                          */
      'xc_mgga_x_scan' :                 263,  # SCAN exchange of Sun, Ruzsinszky, and Perdew                          */
      'xc_mgga_c_scan' :                 267,  # SCAN correlation                                                      */
      'xc_mgga_c_mn15' :                 269,  # MN15 correlation functional from Minnesota                            */
      'xc_mgga_x_b00' :                  284,  # Becke 2000                                                            */
      'xc_mgga_xc_hle17' :               288,  # high local exchange 2017                                              */
      'xc_mgga_c_scan_rvv10' :           292,  # SCAN correlation + rVV10 correlation                                  */
      'xc_mgga_x_revm06_l' :             293,  # revised M06-L exchange functional from Minnesota                      */
      'xc_mgga_c_revm06_l' :             294,  # Revised M06-L correlation functional from Minnesota                   */
      'xc_mgga_x_tm' :                   540,  # Tao and Mo 2016                                                       */
      'xc_mgga_x_vt84' :                 541,  # meta-GGA version of VT{8,4} GGA                                       */
      'xc_mgga_x_sa_tpss' :              542,  # TPSS with correct surface asymptotics                                 */
      'xc_mgga_k_pc07' :                 543,  # Perdew and Constantin 2007                                            */
      'xc_mgga_c_kcis' :                 562,  # Krieger, Chen, Iafrate, and Savin                                     */
      'xc_mgga_xc_lp90' :                564,  # Lee & Parr, Eq. (56)                                                  */
      'xc_mgga_c_b88' :                  571,  # Meta-GGA correlation by Becke                                         */
      'xc_mgga_x_gx' :                   575,  # GX functional of Loos                                                 */
      'xc_mgga_x_pbe_gx' :               576,  # PBE-GX functional of Loos                                             */
      'xc_mgga_x_revscan' :              581,  # revised SCAN                                                          */
      'xc_mgga_c_revscan' :              582,  # revised SCAN correlation                                              */
      'xc_mgga_c_scan_vv10' :            584,  # SCAN correlation +  VV10 correlation                                  */
      'xc_mgga_c_revscan_vv10' :         585,  # revised SCAN correlation                                              */
      'xc_mgga_x_br89_explicit' :        586,  # Becke-Roussel 89 with an explicit inversion of x(y)                   */
      'xc_hyb_mgga_x_dldf' :              36,  # Dispersionless Density Functional                                     */
      'xc_hyb_mgga_x_ms2h' :             224,  # MS2 hybrid exchange of Sun, et al                                     */
      'xc_hyb_mgga_x_mn12_sx' :          248,  # MN12-SX hybrid exchange functional from Minnesota                     */
      'xc_hyb_mgga_x_scan0' :            264,  # SCAN hybrid exchange                                                  */
      'xc_hyb_mgga_x_mn15' :             268,  # MN15 hybrid exchange functional from Minnesota                        */
      'xc_hyb_mgga_x_bmk' :              279,  # Boese-Martin for kinetics                                             */
      'xc_hyb_mgga_x_tau_hcth' :         282,  # Hybrid version of tau-HCTH                                            */
      'xc_hyb_mgga_x_m08_hx' :           295,  # M08-HX exchange functional from Minnesota                             */
      'xc_hyb_mgga_x_m08_so' :           296,  # M08-SO exchange functional from Minnesota                             */
      'xc_hyb_mgga_x_m11' :              297,  # M11 hybrid exchange functional from Minnesota                         */
      'xc_hyb_mgga_x_m05' :              438,  # M05 hybrid exchange functional from Minnesota                         */
      'xc_hyb_mgga_x_m05_2x' :           439,  # M05-2X hybrid exchange functional from Minnesota                      */
      'xc_hyb_mgga_xc_b88b95' :          440,  # Mixture of B88 with BC95 (B1B95)                                      */
      'xc_hyb_mgga_xc_b86b95' :          441,  # Mixture of B86 with BC95                                              */
      'xc_hyb_mgga_xc_pw86b95' :         442,  # Mixture of PW86 with BC95                                             */
      'xc_hyb_mgga_xc_bb1k' :            443,  # Mixture of B88 with BC95 from Zhao and Truhlar                        */
      'xc_hyb_mgga_x_m06_hf' :           444,  # M06-HF hybrid exchange functional from Minnesota                      */
      'xc_hyb_mgga_xc_mpw1b95' :         445,  # Mixture of mPW91 with BC95 from Zhao and Truhlar                      */
      'xc_hyb_mgga_xc_mpwb1k' :          446,  # Mixture of mPW91 with BC95 for kinetics                               */
      'xc_hyb_mgga_xc_x1b95' :           447,  # Mixture of X with BC95                                                */
      'xc_hyb_mgga_xc_xb1k' :            448,  # Mixture of X with BC95 for kinetics                                   */
      'xc_hyb_mgga_x_m06' :              449,  # M06 hybrid exchange functional from Minnesota                         */
      'xc_hyb_mgga_x_m06_2x' :           450,  # M06-2X hybrid exchange functional from Minnesota                      */
      'xc_hyb_mgga_xc_pw6b95' :          451,  # Mixture of PW91 with BC95 from Zhao and Truhlar                       */
      'xc_hyb_mgga_xc_pwb6k' :           452,  # Mixture of PW91 with BC95 from Zhao and Truhlar for kinetics          */
      'xc_hyb_mgga_xc_tpssh' :           457,  # TPSS hybrid                                                           */
      'xc_hyb_mgga_xc_revtpssh' :        458,  # revTPSS hybrid                                                        */
      'xc_hyb_mgga_x_mvsh' :             474,  # MVSh hybrid                                                           */
      'xc_hyb_mgga_xc_wb97m_v' :         531,  # Mardirossian and Head-Gordon                                          */
      'xc_hyb_mgga_xc_b0kcis' :          563,  # Hybrid based on KCIS                                                  */
      'xc_hyb_mgga_xc_mpw1kcis' :        566,  # Modified Perdew-Wang + KCIS hybrid                                    */
      'xc_hyb_mgga_xc_mpwkcis1k' :       567,  # Modified Perdew-Wang + KCIS hybrid with more exact exchange           */
      'xc_hyb_mgga_xc_pbe1kcis' :        568,  # Perdew-Burke-Ernzerhof + KCIS hybrid                                  */
      'xc_hyb_mgga_xc_tpss1kcis' :       569,  # TPSS hybrid with KCIS correlation                                     */
      'xc_hyb_mgga_x_revscan0' :         583,  # revised SCAN hybrid exchange                                          */
      'xc_hyb_mgga_xc_b98' :             598,  # Becke 98                                                              */
   }
   return idDict[name]
