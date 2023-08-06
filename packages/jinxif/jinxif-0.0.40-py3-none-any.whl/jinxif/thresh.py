####
# title: thresh.py
#
# language: Python3.7
# date: 2020-06-00
# license: GPL>=v3
# author: Jenny, bue
#
# description:
#   python3 script to marker threshold
####

# libraries
from jinxif import config
from jinxif import basic
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
from skimage import io, filters
import subprocess
import sys
import time

# developemnt
#import importlib
#importlib.reload()

# global var
s_path_module = os.path.abspath(os.path.dirname(__file__))
s_path_module = re.sub(r'jinxif$','jinxif/', s_path_module)


# functions
def auto_thresh(
        s_slide,
        # filesystem
        s_afsubdir = config.d_nconv['s_afsubdir'],  #'SubtractedRegisteredImages/',  # input and output
        s_format_afsubdir = config.d_nconv['s_format_afsubdir'],  #'{}{}/', # s_afsubdir, s_slide_scene
    ):
    '''
    version: 2021-12-00

    input:
        s_slide: slide id to auto threshold on.

        s_afsubdir: registered or autofluorescence subtracted registered images directory.
        s_format_afsubdir: subfolder structure in s_afsubdir. one subfolder per slide_pxscene

    output:
        csv file in the s_afsubdir folder with threshold information.

    description:
        auto threshold for each slide and marker on af subtracted images.
    '''
    # for the slide generate empty output variable
    b_found = False
    df_thresh = pd.DataFrame()

    # check each folder in afsubdir
    print(f'check for {s_slide} in {s_afsubdir} ...')
    for s_folder in sorted(os.listdir(s_afsubdir)):
        print(f'check {s_folder} ...')
        if s_folder.startswith(s_slide) and os.path.isdir(s_afsubdir+s_folder):
            print(f'process {s_folder} ...')
            b_found = True
            s_afsubpath = s_format_afsubdir.format(s_afsubdir, s_folder)

            # thresh
            df_img = basic.parse_tiff_reg(s_wd=s_afsubpath)
            for s_index in df_img.index:
                s_marker = df_img.loc[s_index,'marker']
                print(f'auto threshold {s_marker} from: {s_index}')

                # get information from pares files
                df_thresh.loc[s_index, df_img.columns] = df_img.loc[s_index, df_img.columns]

                # load file
                # bue 20210803: maybe ai_intensity_image could and should be manipulated to highest 25% expression for nucmem and cellmem!
                ai_intensity_image = io.imread(f'{df_img.index.name}{s_index}')

                # auto threshold
                df_thresh.loc[s_index,'threshold_li'] =  filters.threshold_li(ai_intensity_image)
                if ai_intensity_image.mean() > 0:  # bue 20210611: why you have to check for that?
                    df_thresh.loc[s_index, 'threshold_otsu'] = filters.threshold_otsu(ai_intensity_image)
                    df_thresh.loc[s_index, 'threshold_triangle'] = filters.threshold_triangle(ai_intensity_image)
                #print(df_thresh.info())
                #break

    # write slide output to file
    if b_found:
        s_input = s_afsubdir.split('/')[-2].lower()
        s_ofile = config.d_nconv['s_format_csv_threshold'].format(s_slide, s_input)
        df_thresh.index.name = s_input
        df_thresh.to_csv(s_afsubdir + s_ofile)
        print(f'write file: {s_afsubdir}{s_ofile}')

    else:
        sys.exit(f'Error @ jinxif.extract.thresh.auto_thresh : no sub folder detected for slide {s_slide} in {s_afsubdir}')


def auto_thresh_spawn(
        es_slide,
        # processing
        s_type_processing = 'slurm',
        s_slurm_partition = 'exacloud',
        s_slurm_mem = '32G',
        s_slurm_time = '36:00:00',
        s_slurm_account = 'gray_lab',
        # file system
        s_afsubdir = config.d_nconv['s_afsubdir'],  #'SubtractedRegisteredImages/',
        s_format_afsubdir = config.d_nconv['s_format_afsubdir'],  #'{}{}/', # s_afsubdir, s_slide_pxscene
    ):
    '''
    version: 2021-12-00

    input:
        es_slide: set of slides that should be loaded.

        s_type_processing: string to specify if pipeline is run on a slurm cluster on not.
            known vocabulary is slurm and any other string for non-slurm processing.
        s_slurm_partition: slurm cluster partition to use.
            OHSU ACC options are 'exacloud', 'light', (and 'gpu').
            the default is tweaked to OHSU ACC settings.
        s_slurm_mem: slurm cluster memory allocation. format '64G'.
        s_slurm_time: slurm cluster time allocation in hour or day format.
            OHSU ACC max is '36:00:00' [hour] or '30-0' [day].
            the related qos code is tweaked to OHSU ACC settings.
        s_slurm_account: slurm cluster account to credit time from.
            OHSU ACC options are e.g. 'gray_lab', 'chin_lab', 'CEDAR'.

        s_afsubdir: registered or autofluorescence subtracted registered images directory.
        s_format_afsubdir: subfolder structure in s_afsubdir. one subfolder per slide_pxscene.

    output:
        csv file in the s_afsubdir folder with threshold information.

    description:
        spawner function for thresh.auto_thresh function.
    '''
    # handle input
    s_input = s_afsubdir.split('/')[-2].lower()

    # for each slide
    for s_slide in sorted(es_slide):
        print(f'auto_thresh_spawn: {s_slide} {s_input}')

        # set run commands
        s_pathfile_template = 'template_thresh_slide.py'
        s_pathfile = f'thresh_slide_{s_slide}_{s_input}.py'
        s_srun_cmd = f'python3 {s_pathfile}'
        ls_run_cmd = ['python3', s_pathfile]

        ## any ##
        # load template auto threshold script code
        with open(f'{s_path_module}src/{s_pathfile_template}') as f:
            s_stream = f.read()

        # edit code generic
        s_stream = s_stream.replace('peek_s_slide', s_slide)
        s_stream = s_stream.replace('peek_s_afsubdir', s_afsubdir)
        s_stream = s_stream.replace('peek_s_format_afsubdir', s_format_afsubdir)

        # write executable script code to file
        time.sleep(4)
        with open(s_pathfile, 'w') as f:
            f.write(s_stream)

        # execute script
        time.sleep(4)
        if (s_type_processing == 'slurm'):
            # generate sbatch file
            s_pathfile_sbatch = f'thresh_slide_{s_slide}_{s_input}.sbatch'
            config.slurmbatch(
                s_pathfile_sbatch = s_pathfile_sbatch,
                s_srun_cmd = s_srun_cmd,
                s_jobname = f't{s_slide}',
                s_partition = s_slurm_partition,
                s_gpu = None,
                s_mem = s_slurm_mem,
                s_time = s_slurm_time,
                s_account = s_slurm_account,
            )
            # Jenny, this is cool!
            subprocess.run(
                ['sbatch', s_pathfile_sbatch],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        else:  # non-slurm
            # Jenny, this is cool!
            s_file_stdouterr = f'slurp-thresh_slide_{s_slide}_{s_input}.out'
            o_process = subprocess.run(
                ls_run_cmd,
                stdout=open(s_file_stdouterr, 'w'),
                stderr=subprocess.STDOUT,
            )


def load_thresh_df(
        es_slide,
        i_thresh_manual = 1000,
        s_thresh_marker = 'Ecad',  # can be None!
        # filesystem
        s_afsubdir = config.d_nconv['s_afsubdir'],  #'SubtractedRegisteredImages/',  # input
        # s_format_afsubdir
    ):
    '''
    version: 2021-12-00

    input:
        es_slide: set of slides that should be loaded.
        i_thresh_manual: integer to specify s_thresh_marker threshold value.
        s_thresh_marker: string which specifies the marker to be used cytoplasm detection.
            default is Ecad, since segmentation is usually run on Ecad. adjust if necessary.

        s_afsubdir: registered or autofluorescence subtracted registered images directory.

    output:
        df_img_thresh: dataframe with *_ThresholdLi.csv files specified in es_slide loaded.

    description:
        load threshold files from s_afsubdir.
    '''
    # handle input
    s_input = s_afsubdir.split('/')[-2].lower()

    # load threshold files
    df_img_thresh = pd.DataFrame()
    for s_slide in sorted(es_slide):
        s_file = config.d_nconv['s_format_csv_threshold'].format(s_slide, s_input)
        print(f'Loading: {s_file} ...')
        df_img = pd.read_csv(s_afsubdir + s_file, index_col=0)
        df_img_thresh = df_img_thresh.append(df_img)

    # manually override too low Ecad thresh
    if not (s_thresh_marker is None):
        df_img_thresh.loc[
             (df_img_thresh.marker == s_thresh_marker) & (df_img_thresh.threshold_li < i_thresh_manual),
            'threshold_li'
        ] = i_thresh_manual

    # output
    return(df_img_thresh)


# auto_threshold(
def apply_thresh(
        df_mi,  # from segment.load_cellpose_df
        df_img_thresh,  # from thresh.load_thresh_df
    ):
    '''
    version: 2021-12-00

    input:
        df_mi: dataframe with mean intensity values.
        df_img_thresh: dataframe with threshold values.

    output:
        dfb_thresh: boolean on/off dataframe comprising each marker_partition combination from the df_mi input data frame.

    descrption:
        make a True False dataframe to check thresholds.
    '''
    # check input
    if (df_img_thresh.index.name != df_mi.index.name):
        sys.exit(f'Error @ jinxif.thresh.apply_thresh : df_mi {df_mi.index.name} mean intensity dataframe and df_img_thresh {df_img_thresh.index.name} threshold dataframe seem not to have to same input data source!')

    # generate output files
    dfb_thresh = pd.DataFrame()

    # for each slide_scene (each slide_scene can have different thresholds)
    for s_slidepxscene in sorted(df_mi.slide_scene.unique()):
        print(f'Threshold: {s_slidepxscene}')

        # generate boolean output df according to mean intensity input df
        ls_index_slidescene = sorted(df_mi[df_mi.slide_scene == s_slidepxscene].index)
        dfb_thresh_slidescene = pd.DataFrame(index=ls_index_slidescene)
        dfb_thresh_slidescene['slide'] = s_slidepxscene.split('_')[0]
        dfb_thresh_slidescene['slide_scene'] = s_slidepxscene

        # for each slide_scene's marker apply thresh
        for s_index in df_img_thresh.loc[df_img_thresh.slide_scene == s_slidepxscene,:].index:
            r_thresh = df_img_thresh.loc[s_index, 'threshold_li']
            s_marker = df_img_thresh.loc[s_index, 'marker']
            # for each cell partition
            for s_markerpartition in df_mi.columns[df_mi.columns.str.contains(f"{s_marker}_")]:
                dfb_thresh_slidescene.loc[ls_index_slidescene, s_markerpartition] = df_mi.loc[ls_index_slidescene, s_markerpartition] >= r_thresh
        # update output
        dfb_thresh = dfb_thresh.append(dfb_thresh_slidescene)

    # output
    dfb_thresh.index.name = df_img_thresh.index.name
    return(dfb_thresh)


# threshold scatter plot
def markerpositive_scatterplot(
        s_slidepxscene,
        df_img_thresh,
        dfb_thresh,
        df_xy,
        ls_marker_partition,
        # file system
        s_opath,
    ):
    '''
    version: 2021-12-00

    input:
        s_slidepxscene: one slide_scene identifier.
        df_img_thresh: dataframe with parsed filename and related threshold values.
        dfb_thresh: boolean dataframe with DAPI and s_thresh_marker_partition on/off values for each cell, e.g. generated with auto_threshold.
        df_xy: file with nuclei position.
        ls_marker_partition: list of cell marker_partition to be plotted.

        s_opath: output path where the generated plot should be stored.

    output:
        png plots in the s_opath directory.

    description:
        for marker_parition in s_marker_partition generate marker positive cells location in tissue plots.
    '''
    print(f'thresh.markerpositive_scatterplot processing: {s_slidepxscene} ...')

    # slide_pxscene focus
    df_img_thresh_slidepxscene =  df_img_thresh.loc[df_img_thresh.slide_scene == s_slidepxscene,:]
    dfb_thresh_slidepxscene = dfb_thresh.loc[dfb_thresh.slide_scene == s_slidepxscene,:]
    df_xy_slidepxscene = df_xy.loc[df_xy.slide_scene == s_slidepxscene,:]  # all cells

    # plot
    fig, ax = plt.subplots(2, ((len(ls_marker_partition))+1)//2, sharex=True, figsize=(24,12)) #figsize=(18,12)
    ax = ax.ravel()
    for ax_num, s_marker_partition in enumerate(ls_marker_partition):
        # get marker and threshold
        s_marker = s_marker_partition.split('_')[0]
        r_thresh = df_img_thresh_slidepxscene.loc[df_img_thresh_slidepxscene.marker == s_marker, 'threshold_li']
        print(f'plot marker_partition: {s_marker_partition} {s_marker} {r_thresh}')

        # get positive cells which are positive cells based on threshold
        es_pos_index = set((dfb_thresh_slidepxscene.loc[dfb_thresh_slidepxscene.loc[:, s_marker_partition], :]).index)
        df_cell_pos = df_xy_slidepxscene.loc[df_xy_slidepxscene.index.isin(es_pos_index), :]

        # plot all cells
        ax[ax_num].scatter(data=df_xy_slidepxscene, x='DAPI_X', y='DAPI_Y', color='silver', s=1)
        # plot positive cells
        if len(df_cell_pos) >= 1:
            ax[ax_num].scatter(data=df_cell_pos, x='DAPI_X', y='DAPI_Y', color='DarkBlue', s=.5)
        ax[ax_num].axis('equal')
        ax[ax_num].set_ylim(ax[ax_num].get_ylim()[::-1])
        ax[ax_num].set_title(f'{s_marker} thresh: {int(r_thresh)}')

    # earse empty ax
    for i_ax in range(len(ls_marker_partition), len(ax)):
        ax[i_ax].axis('off')

    # save plot to file
    fig.suptitle(f'{s_slidepxscene} pixel intensity threshold')
    plt.tight_layout()
    ls_save = [s_marker_partition.split('_')[0] for s_marker_partition in ls_marker_partition]
    fig.savefig(s_opath+ f'{s_slidepxscene}_{".".join(ls_save)}_thresh_{df_img_thresh_slidepxscene.index.name}_scatter.png', facecolor='white')
    plt.close()


def markerpositive_scatterplots(
        df_img_thresh,
        dfb_thresh,
        ls_marker_partition,
        es_slide_filter = None,
        # file system
        s_segdir = config.d_nconv['s_segdir'],  #'Segmentation/',
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],  #'{}{}_CellposeSegmentation/', # s_segdir, s_slide
        s_qcdir = config.d_nconv['s_qcdir'],  #'QC/',
    ):
    '''
    version: 2021-12-00

    input:
        df_img_thresh: dataframe with parsed filename and related threshold values.
        dfb_thresh: boolean dataframe with DAPI and s_thresh_marker_partition on/off values for each cell, e.g. generated with auto_threshold.
        ls_marker_partition: list of cell marker_partition to be plotted.
        es_slide_filter: which slides should be processed. if None,all slides present in df_img_thresh will be processed.

        s_segdir: segmentation directory.
        s_format_segdir_cellpose: segmentation folder subdirectory where for each slide the cellpose segmentation results are stored.
        s_qcdir: quality control directory.

    output:
        png plots in the s_qcdir + s_segdir.split('/')[-2]  directory.

    description:
        for marker_partition in s_marker_partition generate marker positive cells location in tissue plots.
    '''
    # handle input
    if es_slide_filter is None:
        es_slide_filter = set(dfb_thresh.slide)

    # handle output path
    s_opath = s_qcdir + s_segdir.split('/')[-2] + '/'
    os.makedirs(s_opath, exist_ok=True)

    # for each slide_pxscene in dfb_thresh
    for s_slidepxscene in sorted(set(dfb_thresh.slide_scene)):
        # detect input folder which can be a registered slide or in a slide-pxscene folder
        print(f'check: {s_slidepxscene} ...')
        b_found = any([s_slidepxscene.startswith(s_slide) for s_slide in es_slide_filter])

        if b_found:
            # load data
            s_slide = s_slidepxscene.split('_')[0]
            s_ipath = s_format_segdir_cellpose.format(s_segdir, s_slide)
            df_xy = pd.read_csv(s_ipath + config.d_nconv['s_format_csv_centroidxy'].format(s_slide), index_col=0)

            # plot
            markerpositive_scatterplot(
                s_slidepxscene = s_slidepxscene,
                df_img_thresh = df_img_thresh,
                dfb_thresh = dfb_thresh,
                df_xy = df_xy,
                ls_marker_partition = ls_marker_partition,
                # file system
                s_opath = s_opath,
            )

