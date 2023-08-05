import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import numpy as np

from ansurr import adjust_text as at

def plot_scores(output_dir='',cyrange=False):
	data = {}
	for line in open(output_dir+'scores.out','r'):
		if line[:4] == 'PDB:':
			line = line.split()
			pdb = line[1][:[pos for pos, char in enumerate(line[1]) if char == '_'][-1]] # accounts for "_" appearing in structure name
			model = int(line[1].split('_')[-1])
			shifts = line[3]
			shift_perc = int(line[5])
			if line[9] != 'nan':
				if pdb not in data:
					if cyrange:
						data[pdb] = {'model':[model],'rmsd':[float(line[13])],'corr':[float(line[9])],'rmsd_welldefined':[float(line[21])],'corr_welldefined':[float(line[17])],'shifts':shifts,'shift_perc':[shift_perc]}
					else:
						data[pdb] = {'model':[model],'rmsd':[float(line[13])],'corr':[float(line[9])],'shifts':shifts,'shift_perc':[shift_perc]}

				else:
					data[pdb]['model'].append(model)
					data[pdb]['rmsd'].append(float(line[13]))
					data[pdb]['corr'].append(float(line[9]))
					data[pdb]['shift_perc'].append(shift_perc)
					if cyrange:
						data[pdb]['rmsd_welldefined'].append(float(line[21]))
						data[pdb]['corr_welldefined'].append(float(line[17]))

				
	for d in enumerate(data):
		plt.figure(d[0])
		plt.scatter(data[d[1]]['rmsd'], data[d[1]]['corr'], c='black',s=8)

		labels = [plt.text(data[d[1]]['rmsd'][i], data[d[1]]['corr'][i], data[d[1]]['model'][i],
						   ha='center', va='center', color='blue',size=6) for i in range(len(data[d[1]]['rmsd']))]

		plt.ylabel('correlation score',size=12)
		plt.xlabel('RMSD score',size=12)
		plt.axis('scaled')  
		plt.xlim(-5,105)
		plt.ylim(-5,105)
		shift_perc = int(round(np.nanmean(data[d[1]]['shift_perc']),0)) # just in case models don't have the same shift completeness - very unlikely
		if shift_perc < 75:
			shift_perc_out = str(shift_perc) + ' (unreliable!)'
		else:
			shift_perc_out = str(shift_perc)

		plt.title('Structure: '+d[1]+'\nShifts: '+data[d[1]]['shifts']+' Shift%: '+shift_perc_out)
		at.adjust_text(labels,expand_text=(1.75, 1.75), expand_points=(1.75, 1.75),arrowprops=dict(arrowstyle='->', color='red', alpha=0.6, linewidth=0.5))
		plt.tight_layout()
		plt.savefig(output_dir+d[1]+'_'+data[d[1]]['shifts']+'.png',dpi=300)


		if cyrange:
			plt.cla()
			plt.scatter(data[d[1]]['rmsd_welldefined'], data[d[1]]['corr_welldefined'], c='black',s=8)
			labels_cyrange = [plt.text(data[d[1]]['rmsd_welldefined'][i], data[d[1]]['corr_welldefined'][i], data[d[1]]['model'][i],
						   ha='center', va='center', color='blue',size=6) for i in range(len(data[d[1]]['rmsd_welldefined']))]

			plt.ylabel('correlation score',size=12)
			plt.xlabel('RMSD score',size=12)
			plt.axis('scaled')  
			plt.xlim(-5,105)
			plt.ylim(-5,105)
			shift_perc = int(round(np.nanmean(data[d[1]]['shift_perc']),0)) # have sep shift completness for well defined region?
			if shift_perc < 75:
				shift_perc_out = str(shift_perc) + ' (unreliable!)'
			else:
				shift_perc_out = str(shift_perc)

			plt.title('Structure: '+d[1]+'\n(WD) Shifts: '+data[d[1]]['shifts']+' Shift%: '+shift_perc_out)
			at.adjust_text(labels_cyrange,expand_text=(1.75, 1.75), expand_points=(1.75, 1.75),arrowprops=dict(arrowstyle='->', color='red', alpha=0.6, linewidth=0.5))
			plt.tight_layout()
			plt.savefig(output_dir+d[1]+'_'+data[d[1]]['shifts']+'_welldefined.png',dpi=300)

def main():

    plot_scores(sys.argv[1])
    sys.exit(0)
   
if __name__ == "__main__":
    main()