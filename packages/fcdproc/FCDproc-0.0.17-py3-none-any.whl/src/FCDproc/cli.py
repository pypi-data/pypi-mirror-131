# -*- coding: utf-8 -*-


import click
import ast
import os
import sys
from copy import deepcopy
import numpy as  np
from FCDproc.workflow.base import Main_FCD_pipeline

class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)
            
            
@click.command()
@click.option('--work_dir', type=click.STRING , help='working directory', required=True)
@click.option('--analysis_mode', type=click.Choice(['preprocess', 'model', 'detect'], case_sensitive=False))
@click.option('--controls', cls=PythonLiteralOption, default=[], help='list of control subject with normal brains')
@click.option('--pt_positive', cls=PythonLiteralOption, default=[], help='list of patients with known fcd lesions')
@click.option('--pt_negative', cls=PythonLiteralOption, default=[], help='list of patients with MRI negative fcd lesions')
@click.option('--fs_reconall/--fs_no_reconall', default=False, help='option to run freesurfer reconstruction')
@click.option('--fs_subjects_dir', type=click.STRING , help='freesurfer subject directory')
@click.option('--fs_license_file', type=click.STRING , help='freesurfer license key file location')
@click.option('--output_dir', type=click.STRING , help='output data directory',required=True)
@click.option('--bids_dir', type=click.STRING , help='input data directory', required=True)

def Create_FCD_Pipeline(bids_dir, output_dir, work_dir, analysis_mode, controls, pt_positive, pt_negative, fs_reconall, fs_license_file, fs_subjects_dir):
    """ create fcd pipeline that can perform sinlge subject processing, modeling and detecting of FCD lesion"""
    
    click.echo(f"performing {analysis_mode} analysis")
    pipeline = Main_FCD_pipeline(bids_dir, output_dir, work_dir, analysis_mode, controls, pt_positive, pt_negative, fs_reconall, fs_license_file, fs_subjects_dir)
    pipeline.run(plugin='Linear')

    