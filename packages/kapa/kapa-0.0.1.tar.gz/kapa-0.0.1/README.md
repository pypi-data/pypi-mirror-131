There are two main functions in this package, "kapa", is coded for performing kinase activity profiling analysis, while "conv_MQtable" is built for converting MaxQuant outputs to stardard input of "kinenrich".


The site.csv and protein.csv can be used to test the kapa function

kapa(siteratio_dir = current_directory+'site.csv', input_type = 'protein', output_dir = desired_output_directory, exp_label='', proratio_dir=current_directory+'protein.csv',  output_ratio=False, log2trans=True) 


Parameters of kapa 
kapa(siteratio_dir, input_type, output_dir, exp_label='', proratio_dir="None",  output_ratio=False, log2trans=True) 

Perform kinase activity profiling analysis based on ratio of kinase substrates
Parameters can be customized through key-value pairs as below.

Parameters:
siteratio_dir: string
The directory of the file that contains the ratio of every site.

input_type: {“UniprotAC” or “protein”, “gene symbol” or “gene”}
The type of IDs used in the site ratio file and the protein ratio file, format in both files should be the same. 
 "UniprotAC" or "protein"   example: Q00987, P40337, Q9HAU4, O43791
 "gene symbol" or "gene"   example: MDM2, VHL, SMUF2, SPOP
List of valid input and examples will be shown if it is an invalid value.

output_dir: string
The directory where kinase enrichment result files will be generated.

exp_label: string, default ""
The string attached to the output file name that separates different results when there are multiple groups. 

proratio_dir: string, default ""
The directory of the file that contains the ratio of every protein. A valid directory input here will trigger normalization by corresponding protein ratio for all files in this run. By default, the output will not be normalized by protein ratio.

ratio_output: bool, default False
If True, files that contain the ratio of each ubiquitylation site and the average ratio of each ubiquitinated protein will be generated. 

log2trans: bool, default True
If True, ratios will take transform y=log2(x) before the E3 ligase enrichment analysis. If False, the ratio from files will be used for enrichment analysis directly. 
 
Returns:
This function generates files based on E3 ligase enrichment results and does not have any returns.





Parameters of conv_MQtable
conv_MQtable(file_source,output_dir,siteorpro,exp_label="",output_label="")

Convert MaxQuant outputs to standard input of kinenrich function
Parameters can be customized through key-value pairs as below.

file_source: string
The directory of the file that needs to be converted.

output_dir: string
The directory where convertion output files will be generated.

exp_label: string, default ""
The string used to tell which experiment or which column to be selected and written into output. 

output_label: string, default ""
The string attached to the output file name that separates different results when there are multiple groups. Note:no "/" allowed  
 
Returns:
This function generates converted ratio files in selected directory and does not have any returns.