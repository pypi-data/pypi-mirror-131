#!/usr/local/bin/ python3
# This module contains a set of functions and classes that are used in several different Python scripts in the Database.

from astropy.utils.data import download_file,clear_download_cache
from astropy.io import fits
from collections import OrderedDict #used in Proper_Dictionary
import copy # Used in columndensities
import numpy as np # Used in convertskyangle and columndensity and
import os

from pyHIARD import Templates as templates
from pyHIARD.AGC.base_galaxies import Base_Galaxy
try:
    import importlib.resources as import_res
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as import_res
import re
import subprocess
from scipy.ndimage import gaussian_filter
import signal
import traceback

class SofiaFaintError(Exception):
    pass
class SofiaRunError(Exception):
    pass
# A class of ordered dictionary where keys can be inserted in at specified locations or at the end.
class Proper_Dictionary(OrderedDict):
    def insert(self, existing_key, new_key, key_value):
        done = False
        if new_key in self:
            self[new_key] = key_value
            done = True
        else:
            new_orderded_dict = self.__class__()
            for key, value in self.items():
                new_orderded_dict[key] = value
                if key == existing_key:
                    new_orderded_dict[new_key] = key_value
                    done = True
            if not done:
                new_orderded_dict[new_key] = key_value
                done = True
                print(
                    "----!!!!!!!! YOUR new key was appended at the end as you provided a non-existing key to add it after!!!!!!---------")
            self.clear()
            self.update(new_orderded_dict)

        if not done:
            print("----!!!!!!!!We were unable to add your key!!!!!!---------")
#Function to convert column densities

def check_input(cfg):
    #Check the main directory exists
    while not os.path.isdir(cfg.general.main_directory):
        print(f'The directory {cfg.general.main_directory} does not exist please provide the correct directory')
        cfg.general.main_directory = input("Please provide the directory where to create the database :")
    #if we want the full database default we check that the user wants this
    if cfg.general.main_directory[-1] != '/':
        cfg.general.main_directory = f"{cfg.general.main_directory}/"

    if cfg.agc.enable:
        cfg.general.tirific = find_program(cfg.general.tirific,'TiRiFiC')
        if cfg.agc.corruption_method.lower() in ['casa_sim','casa_5']:
            cfg.general.casa = find_program(cfg.general.casa,'CASA')
    if cfg.roc.enable:
        cfg.general.sofia2 = find_program(cfg.general.sofia2,'SoFiA2')

    if cfg.agc.enable:

        #sets = 5  # This is the amount of base galaxies we want, i.e. the number of rotation curves
        question_base = False
        for gals in cfg.agc.base_galaxies:
            if not 1 <= gals <= 6:
                question_base =True
        if question_base:
            print(f'''Please select the base types you would like to use''')
            for i in range(1,6):
                print(f'''{i}) Galaxy {i} has the following Base parameters to vary on.''')
                cf.print_base_galaxy(Base_Galaxy(i))

            vals = input(f"Or you can construct you own by selecting 6, default = 6: ")
            if vals == '':
                cfg.agc.base_galaxies = [6]
            else:
                cfg.agc.base_galaxies = [int(x)  for x in re.split("\s+|\s*,\s*|\s+$",vals.strip()) if 1 <=  int(x) <= 6]
                if len(cfg.agc.base_galaxies) == 0:
                    cfg.agc.base_galaxies = [6]
        while cfg.agc.corruption_method.lower() not in ['casa_sim', 'gaussian', 'casa_5']:
            cfg.agc.corruption_method = input('Your method of corruption is not acceptable please choose from Casa_Sim, Gaussian, Casa_5 (Default = Gaussian):')
            if cfg.agc.corruption_method == '':
                cfg.agc.corruption_method = 'Gaussian'

        if cfg.agc.corruption_method.lower() == 'casa_sim' or cfg.agc.corruption_method.lower() == "c_s":
            cfg.agc.corruption_method = 'Casa_Sim'
            print("You are using the casa corruption method please make sure python can access casa.")
        elif  cfg.agc.corruption_method .lower() == 'gaussian' or cfg.agc.corruption_method  == "" or cfg.agc.corruption_method .lower() == 'g' :
            cfg.agc.corruption_method  = 'Gaussian'
        elif cfg.agc.corruption_method .lower() == 'casa_5' or cfg.agc.corruption_method .lower() == "c_5":
            cfg.agc.corruption_method  = 'Casa_5'
            print("You are using the casa corruption method please make sure python can access casa.")

        question_variations = False
        changes_poss = ['Inclination', 'PA','Beams','Radial_Motions','Flare','Arms','Bar','Channelwidth','SNR','Warp','Mass','Beam_Resolution','Base']
        changes_poss_lower = [x.lower() for x in changes_poss]
        for i,variables in enumerate(cfg.agc.variables_to_vary):
            while variables.lower() not in changes_poss_lower:
                variables = input(f'''{variables} is not a legitimate variable to variations.
Please choose from {','.join([x for x in changes_poss])}
replace with:''')

            cfg.agc.variables_to_vary[i] = changes_poss[changes_poss_lower.index(variables.lower())]
        #We always make the base
        if 'Base' not in cfg.agc.variables_to_vary:
            cfg.agc.variables_to_vary.append('Base')

        if 'inclination' in [x.lower() for x in cfg.agc.variables_to_vary]:
            for i,incs in enumerate(cfg.agc.inclination):
                while not 0. <= incs <= 90.:
                    incs = float(input(f'please choose a value between 0.- 90.:'))
                cfg.agc.inclination[i] = incs
        if 'pa' in [x.lower() for x in cfg.agc.variables_to_vary]:
            for i,incs in enumerate(cfg.agc.pa):
                while not 0. <= incs <= 360.:
                    incs = float(input(f'please choose a value between 0.- 360.:'))
                cfg.agc.pa[i] = incs



    if cfg.roc.enable:

        allowed_galaxies = ['M_83','Circinus','NGC_5023','NGC_2903','NGC_3198','NGC_5204','UGC_1281','UGC_7774']
        allowed_galaxies_low = [x.lower() for x in allowed_galaxies]
        for i,galaxy in enumerate(cfg.roc.base_galaxies):
            while galaxy.lower() not in allowed_galaxies_low:
                galaxy = input(f'''{galaxy} is not a legitimate galaxy to vary.
Please choose from {','.join([x for x in allowed_galaxies])}
replace with:''')
            cfg.roc.base_galaxies[i] = allowed_galaxies[allowed_galaxies_low.index(galaxy.lower())]
        changes_poss = ['Beams','SNR']
        changes_poss_lower = [x.lower() for x in changes_poss]
        for i,variables in enumerate(cfg.roc.variables_to_vary):
            while variables.lower() not in changes_poss_lower:
                variables = input(f'''{variables} is not a legitimate variable to variations.
Please choose from {','.join([x for x in changes_poss])}
replace with:''')

            cfg.roc.variables_to_vary[i] = changes_poss[changes_poss_lower.index(variables.lower())]
    if cfg.roc.enable and cfg.roc.delete_existing:
        to_delete  =f'''rm -R {' '.join([f"{cfg.general.main_directory}{x}_*Beams_*SNR" for x in cfg.roc.base_galaxies])}'''
        print("All previous models of the requested base galaxies will be removed prior to the build. \n")

        print(f"The command {to_delete} will be run.")
        cfg.roc.delete_existing = get_bool("Are you sure you want to do this? (Yes/No, default=No): ",default=False)

    return cfg
check_input.__doc__ =f'''
 NAME:
    check_input

 PURPOSE:
    Check the configuration input and that all required input is present.
    In case of missing input request the input from the user.

 CATEGORY:
    common_functions

 INPUTS:
    outdir = directory where to put the final masks for future use
    working_dir = directory where to run sofia
    name = Base name of the input and output files

 OPTIONAL INPUTS:
    sofia_call = command name to run sofia

 OUTPUTS:
    the cut cube is returned.

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''


def columndensity(levels,systemic = 100.,beam=[1.,1.],channel_width=1.,column= False,arcsquare=False,solar_mass =False):
    #set solar_mass to indicate the output should be M_solar/pc**2 or if column = True the input is
    f0 = 1.420405751786E9 #Hz rest freq
    c = 299792.458 # light speed in km / s
    pc = 3.086e+18 #parsec in cm
    solarmass = 1.98855e30 #Solar mass in kg
    mHI = 1.6737236e-27 #neutral hydrogen mass in kg

    if systemic > 10000:
        systemic = systemic/1000.
    f = f0 * (1 - (vsys / c)) #Systemic frequency
    if arcsquare:
        HIconv = 605.7383 * 1.823E18 * (2. *np.pi / (np.log(256.)))
        if column:
            # If the input is in solarmass we want to convert back to column densities
            if solar_mass:
                levels=levels*solarmass/(mHI*pc**2)
            #levels=levels/(HIconv*channel_width)
            levels = levels/(HIconv*channel_width)
        else:

            levels = HIconv*levels*channel_width
            if solar_mass:
                levels = levels/solarmass*(mHI*pc**2)
    else:
        if beam.size <2:
            beam= [beam,beam]
        b=beam[0]*beam[1]
        if column:
            if solar_mass:
                levels=levels*solarmass/(mHI*pc**2)
            TK = levels/(1.823e18*channel_width)
            levels = TK/(((605.7383)/(b))*(f0/f)**2)
        else:
            TK=((605.7383)/(b))*(f0/f)**2*levels
            levels = TK*(1.823e18*channel_width)
    if ~column and solar_mass:
        levels = levels*mHI*pc**2/solarmass
    return levels
        # a Function to convert the RA and DEC into hour angle (invert = False) and vice versa (default)
def convertRADEC(RA,DEC,invert=False, colon=False):

    if not invert:
        try:
            _ = (e for e in RA)
        except TypeError:
            RA= [RA]
            DEC =[DEC]
        for i in range(len(RA)):
            xpos=RA
            ypos=DEC
            xposh=int(np.floor((xpos[i]/360.)*24.))
            xposm=int(np.floor((((xpos[i]/360.)*24.)-xposh)*60.))
            xposs=(((((xpos[i]/360.)*24.)-xposh)*60.)-xposm)*60
            yposh=int(np.floor(np.absolute(ypos[i]*1.)))
            yposm=int(np.floor((((np.absolute(ypos[i]*1.))-yposh)*60.)))
            yposs=(((((np.absolute(ypos[i]*1.))-yposh)*60.)-yposm)*60)
            sign=ypos[i]/np.absolute(ypos[i])
            if colon:
                RA[i]="{}:{}:{:2.2f}".format(xposh,xposm,xposs)
                DEC[i]="{}:{}:{:2.2f}".format(yposh,yposm,yposs)
            else:
                RA[i]="{}h{}m{:2.2f}".format(xposh,xposm,xposs)
                DEC[i]="{}d{}m{:2.2f}".format(yposh,yposm,yposs)
            if sign < 0.: DEC[i]='-'+DEC[i]
        if len(RA) == 1:
            RA = str(RA[0])
            DEC = str(DEC[0])
    else:
        if isinstance(RA,str):
            RA=[RA]
            DEC=[DEC]

        xpos=RA
        ypos=DEC

        for i in range(len(RA)):
            # first we split the numbers out
            tmp = re.split(r"[a-z,:]+",xpos[i])
            RA[i]=(float(tmp[0])+((float(tmp[1])+(float(tmp[2])/60.))/60.))*15.
            tmp = re.split(r"[a-z,:'\"]+",ypos[i])
            DEC[i]=float(np.absolute(float(tmp[0]))+((float(tmp[1])+(float(tmp[2])/60.))/60.))*float(tmp[0])/np.absolute(float(tmp[0]))

        if len(RA) == 1:
            RA= float(RA[0])
            DEC = float(DEC[0])
    return RA,DEC


# function for converting kpc to arcsec and vice versa

def convertskyangle(angle, distance=1., unit='arcsec', distance_unit='Mpc', physical=False):
    try:
        _ = (e for e in angle)
    except TypeError:
        angle = [angle]

        # if physical is true default unit is kpc
    angle = np.array(angle)
    if physical and unit == 'arcsec':
        unit = 'kpc'
    if distance_unit.lower() == 'mpc':
        distance = distance * 10 ** 3
    elif distance_unit.lower() == 'kpc':
        distance = distance
    elif distance_unit.lower() == 'pc':
        distance = distance / (10 ** 3)
    else:
        print('CONVERTSKYANGLE: ' + distance_unit + ' is an unknown unit to convertskyangle.\n')
        print('CONVERTSKYANGLE: please use Mpc, kpc or pc.\n')
        sys.exit()
    if not physical:
        if unit.lower() == 'arcsec':
            radians = (angle / 3600.) * ((2. * np.pi) / 360.)
        elif unit.lower() == 'arcmin':
            radians = (angle / 60.) * ((2. * np.pi) / 360.)
        elif unit.lower() == 'degree':
            radians = angle * ((2. * np.pi) / 360.)
        else:
            print('CONVERTSKYANGLE: ' + unit + ' is an unknown unit to convertskyangle.\n')
            print('CONVERTSKYANGLE: please use arcsec, arcmin or degree.\n')
            sys.exit()

        kpc = 2. * (distance * np.tan(radians / 2.))
    else:
        if unit.lower() == 'kpc':
            kpc = angle
        elif unit.lower() == 'mpc':
            kpc = angle / (10 ** 3)
        elif unit.lower() == 'pc':
            kpc = angle * (10 ** 3)
        else:
            print('CONVERTSKYANGLE: ' + unit + ' is an unknown unit to convertskyangle.\n')
            print('CONVERTSKYANGLE: please use kpc, Mpc or pc.\n')
            sys.exit()
        radians = 2. * np.arctan(kpc / (2. * distance))
        kpc = (radians * (360. / (2. * np.pi))) * 3600.
    if len(kpc) == 1:
        kpc = float(kpc[0])
    return kpc

def create_masks(outdir,working_dir,name,sofia_call='sofia2'):
    Cube=fits.open(f"{outdir}/{name}.fits",uint = False, do_not_scale_image_data=True,ignore_blank = True)
    data= Cube[0].data
    hdr = Cube[0].header
    Cube.close()
    # First we smooth our template
    # We smooth this to 1.25 the input beam
    bmaj=hdr["BMAJ"]*3600.
    bmin=hdr["BMIN"]*3600.
    FWHM_conv_maj = np.sqrt((1.25 * bmaj) ** 2 - bmaj ** 2)
    FWHM_conv_min = np.sqrt((1.25 * bmin) ** 2 - bmin ** 2)
    # and in terms of pixels the sigmas
    sig_maj = (FWHM_conv_maj / np.sqrt(8 * np.log(2))) / abs(hdr["CDELT1"] * 3600.)
    sig_min = (FWHM_conv_min / np.sqrt(8 * np.log(2))) / abs(hdr["CDELT2"] * 3600.)
    #We replace zeros with NAN
    data[data == 0.] = float('NaN')
    Tmp_Cube = gaussian_filter(data, sigma=(0, sig_min, sig_maj), order=0)
    # Replace 0. with Nan

    #write this to the fits file
    fits.writeto(f'{working_dir}/tmp.fits', Tmp_Cube, hdr,overwrite=True)
    SoFiA_Template = read_template_file('Sofia_Template.par')
    SoFiA_Template['input.data'.upper()] = f'input.data = {working_dir}/tmp.fits'
    SoFiA_Template['scfind.threshold'.upper()]= 'scfind.threshold	= 7'
    SoFiA_Template['linker.minSizeZ'.upper()]=  f'linker.minSizeZ = {int(Tmp_Cube.shape[0]/2.)}'
    with open(f'{working_dir}/tmp_sof.par', 'w') as file:
        file.writelines([SoFiA_Template[key] + "\n" for key in SoFiA_Template])
    run_sofia(working_dir,'tmp_sof.par',sofia_call = sofia_call)

    Mask_Outer = fits.open(working_dir + '/tmp_mask.fits')
    Mask_Outer[0].header['CUNIT3'] = 'KM/S'
    try:
        del Mask_Outer[0].header['HISTORY']
    except:
        pass
    fits.writeto(f'{outdir}/Outer_{name}_mask.fits',Mask_Outer[0].data,Mask_Outer[0].header,overwrite = True)
    os.system(f"rm -f {working_dir}/tmp_mask.fits")
    # Create the inner mask
    SoFiA_Template['dilation.enable'.upper()]='dilation.enable	=	false'
    with open(f'{working_dir}/tmp_sof.par', 'w') as file:
        file.writelines([SoFiA_Template[key] + "\n" for key in SoFiA_Template])
    run_sofia(working_dir,'tmp_sof.par',sofia_call = sofia_call)


    Mask_Inner = fits.open(working_dir + '/tmp_mask.fits')
    Mask_Inner[0].header['CUNIT3'] = 'KM/S'
    del Mask_Inner[0].header['HISTORY']
    fits.writeto(f'{outdir}/Inner_{name}_mask.fits',Mask_Inner[0].data,Mask_Inner[0].header,overwrite = True)
    os.system(f"rm -f {working_dir}/tmp_mask.fits")
    os.system(f"rm -f {working_dir}/tmp.fits")
    os.system(f'rm -f {working_dir}/tmp_sof.par')
    return Mask_Inner,Mask_Outer
create_masks.__doc__ =f'''
 NAME:
    create_masks

 PURPOSE:
    Create the masks for the ROC standards.

 CATEGORY:
    common_functions

 INPUTS:
    outdir = directory where to put the final masks for future use
    working_dir = directory where to run sofia
    name = Base name of the input and output files

 OPTIONAL INPUTS:
    sofia_call = command name to run sofia

 OUTPUTS:
    the cut cube is returned.

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''


def cut_input_cube(file_in,sizes,debug=False):
    cube = fits.open(file_in,uint=False, do_not_scale_image_data=True,ignore_blank=True)
    hdr = cube[0].header
    for i,pos in enumerate(sizes):
        if pos[1] == -1:
            sizes[i][1]=hdr[f'NAXIS{3-i}']-1

    if hdr['NAXIS'] > 3:
        hdr['NAXIS'] =3
        del hdr['*4']
        new_data = cube[0].data[0,sizes[0][0]:sizes[0][1],sizes[1][0]:sizes[1][1],sizes[2][0]:sizes[2][1]]
    else:
        new_data = cube[0].data[sizes[0][0]:sizes[0][1],sizes[1][0]:sizes[1][1],sizes[2][0]:sizes[2][1]]

    if f'PC01_01' in hdr:
        del hdr['PC0*_0*']
    hdr['NAXIS1']= sizes[2][1]-sizes[2][0]
    hdr['NAXIS2']= sizes[1][1]-sizes[1][0]
    hdr['NAXIS3']= sizes[0][1]-sizes[0][0]

    hdr['CRPIX1']=hdr['CRPIX1']-sizes[2][0]
    hdr['CRPIX2']=hdr['CRPIX2']-sizes[1][0]
    hdr['CRPIX3']=hdr['CRPIX3']-sizes[0][0]
    try:
        del Mask_Outer[0].header['HISTORY']
    except:
        pass
    if hdr['BITPIX'] < -32:
        print(hdr['BITPIX'])
        exit()
    elif hdr['BITPIX'] > -32:
        hdr['BITPIX'] = 32
    cube[0].header=hdr
    cube[0].data=np.array(new_data,dtype=float)
    return cube
cut_input_cube.__doc__ =f'''
 NAME:
    cut_input_cube

 PURPOSE:
    Cut filename back to the size of subcube, update the header and write back to disk.

 CATEGORY:
    common_functions

 INPUTS:
    file_in = the fits file to cut
    sizes = array that contains the new size as
                [[z_min,z_max],[y_min,y_max], [x_min,x_max]]
                adhering to fits' idiotic way of reading fits files.


 OPTIONAL INPUTS:
    debug = False

 OUTPUTS:
    the cut cube is returned.

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''

def download_cube(name,url,sizes,new_location):
    name_in = download_file(url,pkgname='pyHIARD')
    cube = cut_input_cube(name_in,sizes)
    fits.writeto(f'{new_location}/{name}.fits',cube[0].data,cube[0].header)
    clear_download_cache(url,pkgname='pyHIARD')
    return cube
download_cube.__doc__ =f'''
 NAME:
    download_cube

 PURPOSE:
    Download the specified cube when not present in installation and cut down required size
    Store in installation for future use.

 CATEGORY:
    common_functions

 INPUTS:
    name = local name of the cube
    url = url of location of remote cube
    sizes = require sizes for stored cube
    new_location = location of correct directory in installation.


 OPTIONAL INPUTS:
    debug = False

 OUTPUTS:
    the cut cube is returned

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''

def find_program(name,search):
    found = False
    while not found:
        try:
            run = subprocess.Popen([name], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            run.stdout.close()
            run.stderr.close()
            os.kill(run.pid, signal.SIGKILL)
            found = True
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            name = input(f'''You have indicated to use {name} for using {search} but it cannot be found.
Please provide the correct name : ''')
    return name

find_program.__doc__ =f'''
 NAME:
    find_program

 PURPOSE:
    check whether a program is available for use.

 CATEGORY:
    support_functions

 INPUTS:
    name = command name of the program to run
    search = Program we are looking for
 OPTIONAL INPUTS:

 OUTPUTS:
    the correct command for running the program

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''

# Function to input a boolean answer
def get_bool(print_str="Please type True or False",default=True):
    invalid_input = True
    while invalid_input:
        inp = input(print_str)
        if inp == "":
            if default:
                return True
            else:
                return False
        elif inp.lower() == "true" or inp.lower() == "t" or inp.lower() == "y" or inp.lower() == "yes":
            return True
        elif inp.lower() == "false" or inp.lower() == "f" or inp.lower() == "n" or inp.lower() == "no":
            return False
        else:
            print("Error: the answer must be true/false or yes/no.")
#Function for loading the variables of a tirific def file into a set of variables to be used
def load_tirific(name,Variables = ['BMIN','BMAJ','BPA','RMS','DISTANCE','NUR','RADI','VROT',
                 'Z0', 'SBR', 'INCL','PA','XPOS','YPOS','VSYS','SDIS','VROT_2',  'Z0_2','SBR_2',
                 'INCL_2','PA_2','XPOS_2','YPOS_2','VSYS_2','SDIS_2','CONDISP','CFLUX','CFLUX_2'],
                 unpack = True ):

    model = __import__(f'pyHIARD.Resources.Cubes.{name}', globals(), locals(), name,0)
    with import_res.open_text(model, f'{name}.def') as tmp:
        unarranged = tmp.readlines()


    Variables = np.array([e.upper() for e in Variables],dtype=str)
    numrings = [int(e.split('=')[1].strip()) for e in unarranged if e.split('=')[0].strip().upper() == 'NUR']
    outputarray=np.zeros((numrings[0],len(Variables)),dtype=float)

    # Separate the keyword names
    for line in unarranged:
        var_concerned = str(line.split('=')[0].strip().upper())
        if len(var_concerned) < 1:
            var_concerned = 'xxx'
        varpos = np.where(Variables == var_concerned)[0]
        if varpos.size > 0:
            tmp =  np.array(line.split('=')[1].rsplit(),dtype=float)
            outputarray[0:len(tmp),int(varpos)] = tmp[0:len(tmp)]
        else:
            if var_concerned[0] == '#':
                varpos = np.where(var_concerned[2:] == Variables)[0]
                if varpos.size > 0:
                    tmp = np.array(line.split('=')[1].rsplit(),dtype=float)
                    outputarray[0:len(tmp),int(varpos)] = tmp[:]
    if unpack:
        return (*outputarray.T,)
    else:
        return outputarray

def print_base_galaxy(Galaxy):
    print(f'''{'Inclination':15s} = {Galaxy.Inclination:<10.1f}, {'Dispersion':15s} = {Galaxy.Dispersion}
{'Mass':15s} = {Galaxy.Mass:<10.2e}, {'PA':15s} = {Galaxy.PA}
{'Flare':15s} = {Galaxy.Flare:10s}, {'Warp':15s} = {Galaxy.Warp}
{'Beams':15s} = {Galaxy.Beams:<10.1f}, {'SNR':15s} = {Galaxy.SNR}
{'Channelwidth':15s} = {Galaxy.Channelwidth:<10.1f}, {'Coord':15s} = {Galaxy.Coord}
{'Arms':15s} = {Galaxy.Arms:10s}, {'Res_Beam':15s} = {Galaxy.Res_Beam}
{'Bar':15s} = {Galaxy.Bar:10s}, {'Radial_Motions':15s} = {Galaxy.Radial_Motions}
''')

print_base_galaxy.__doc__=f''' NAME:
    print_base_galaxy

 PURPOSE:
    print the contents of a galaxy class in an orderly fashion

 CATEGORY:
    common_functions

 INPUTS:
    galaxy class

 OPTIONAL INPUTS:

 OUTPUTS:
    print out of the galaxies parameters.

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
 '''

def read_template_RC(name,type= 'RC'):
    #temp = __import__('spam.ham', globals(), locals(), ['eggs', 'sausage'], 0)
    model = __import__(f'pyHIARD.Resources.Cubes.{name}', globals(), locals(), name,0)
    with import_res.open_text(model, f'{name}.rotcur') as tmp:
        unarranged = tmp.readlines()

    Template_in = Proper_Dictionary({})
    counter = 0.
    # Separate the keyword names
    values=[]
    for tmp in unarranged:
        if tmp[0] != '!':
            range = tmp.split()
            if counter == 0:
                for item in range:
                    values.append([float(item)])
                counter = 1.
            else:
                for i,item in enumerate(range):
                    values[i].append(float(item))
    return np.array(values)



def read_template_file(filename):
    with import_res.open_text(templates, filename) as tmp:
        unarranged = tmp.readlines()
    Template_in = Proper_Dictionary({})

    # Separate the keyword names
    for tmp in unarranged:
        # python is really annoying with needing endlines. Let's strip them here and add them when writing
        Template_in[tmp.split('=',1)[0].strip().upper()]=tmp.rstrip()
    return Template_in


def read_casa_template(filename):
    with import_res.open_text(templates, filename) as tmp:
        unarranged = tmp.readlines()
    Template_Casa_In = Proper_Dictionary({})
    # Separate the keyword names
    current_task="pre_task"
    counter=0
    tasks=["pre_task"]
    task_counter = 0
    #deccounter = 0
    #decin= np.arange(43.951946,84,5.)
    for tmp in unarranged:
    # python is really annoying with needing endlines. Let's strip them here and add them when writing
        if re.split('\(|\)',tmp)[0] == 'default':
            task_counter = 0
            for_task = 0
            current_task=re.split('\(|\)',tmp)[1]
            while current_task in tasks:
                for_task += 1
                current_task=re.split('\(|\)',tmp)[1]+"_{:d}".format(for_task)
            tasks.append(current_task)
        if len(tmp.split('=',1)) >1:
            variable=tmp.split('=',1)[0].strip().lower()
            same_var = 0
            while current_task+'_'+variable in Template_Casa_In:
                same_var += 1
                variable=tmp.split('=',1)[0].strip().lower()+"_{:d}".format(same_var)
        elif len(tmp.split('#',1)) >1:
            counter+=1
            variable = "comment_{:d}".format(counter)
        else:
            task_counter +=1
            variable = "run_{:d}".format(task_counter)
        Template_Casa_In[current_task+'_'+variable]=tmp.rstrip()
    return Template_Casa_In

read_casa_template.__doc__=f'''
 NAME:
    read_casa_template

 PURPOSE:
    read a casa template file into a proper dictionary

 CATEGORY:
    common_functions

 INPUTS:
    filename = name of the template file

 OPTIONAL INPUTS:

 OUTPUTS:
    Organized template dictionary
 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
 '''
#Function to read simple input files that  use = as a separator between ithe required input and the values
def read_input_file(filename):


    tmpfile = open(filename, 'r')
    File = Proper_Dictionary({})
    unarranged = tmpfile.readlines()
    # Separate the keyword names
    for tmp in unarranged:
        # python is really annoying with needing endlines. Let's strip them here and add them when writing
        File[tmp.split('=', 1)[0].strip().upper()] = tmp.rstrip()
    return File

def run_sofia(working_dir,parameter_file,sofia_call = 'sofia2'):
    sfrun = subprocess.Popen([sofia_call,parameter_file],cwd=working_dir, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    sofia_run, sofia_warnings_are_annoying = sfrun.communicate()
    print(sofia_run.decode("utf-8"))
    if sfrun.returncode == 8:
        raise SofiaFaintError("RUN_SOFIA:Sofia cannot find a source in the input cube")
    elif sfrun.returncode == 0:
        sofia_ok = True
    else:
        print(sofia_warnings_are_annoying.decode("utf-8"))
        raise SofiaRunError("RUN_SOFIA:Sofia did not execute properly. See screen for details")
run_sofia.__doc__ =f'''
 NAME:
    run_sofia

 PURPOSE:
    run sofia

 CATEGORY:
    common_functions

 INPUTS:
    working_dir = directory where to run sofia
    parameter_file = input parameters file for sofia


 OPTIONAL INPUTS:
    sofia_call = command name for running sofia

 OUTPUTS:

 OPTIONAL OUTPUTS:

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''
