from pyneuroml import pynml
import urllib.request, json 
import requests
import os
from pyneuroml.analysis.NML2ChannelAnalysis import run
from neuroml import *
from neuroml.utils import component_factory
import neuroml.writers as writers
from neuroml import loaders
from pyneuroml import pynml





types = {'cell':'NMLCL','channel':'NMLCH'}

#Helper method for search
def search_neuromldb(search_term, type=None):
    
    with urllib.request.urlopen('https://neuroml-db.org/api/search?q=%s' % search_term.replace(' ','%20')) as url:
        data = json.load(url)

    for l in data:
        if type!=None:
            for type_ in types:
                if type==type_ and not types[type_] in l['Model_ID']:
                    data.remove(l)
        if l in data:
            print('%s: %s, %s %s %s'%(l['Model_ID'],l['Name'],l['First_Author'],l['Second_Author'],l['Publication_Year']))
        
    return data

#data = search_neuromldb("Fast Sodium", 'channel')

# Helper method to retrieve a NeuroML file based on modelID
def get_model_from_neuromldb(model_id, type):
  
    fname = '%s.%s.nml'%(model_id, type)

    url = 'https://neuroml-db.org/render_xml_file?modelID=%s'%model_id
    r = requests.get(url, verify=False)
    with open(fname , 'wb') as f:
        f.write(r.content)

    return pynml.read_neuroml2_file(fname), fname


# Choose one of the channels
#chan_model_id = 'NMLCH001490'

#na_chan_doc, na_chan_fname_orig = get_model_from_neuromldb(chan_model_id, 'channel')

#na_chan = na_chan_doc.ion_channel[0] # select the first/only ion channel in the nml doc

#na_chan_fname = '%s.channel.nml'%na_chan.id
#os.rename(na_chan_fname_orig, na_chan_fname) # Rename for clarity

#print('Channel %s (in file %s) has notes: %s'%(na_chan.id, na_chan_fname, na_chan.notes))

#   TEST!!!
na_erev = 50 # mV
#run(channel_files=["C:/Neurosim/NaTs.channel.nml"], ivCurve=True, erev=na_erev, clampDelay=5, clampDuration=10, duration=20)



#data = search_neuromldb("Fast Potassium", 'channel')

# Download one of these

#k_chan_doc, k_chan_fname_orig = get_model_from_neuromldb('NMLCH001529', 'channel')

#k_chan = k_chan_doc.ion_channel[0] # select the first ion channel in the nml doc

#k_chan_fname = '%s.channel.nml'%k_chan.id
#os.rename(k_chan_fname_orig, k_chan_fname) # Rename for clarity

#print('Channel %s (in file %s) has notes: %s'%(k_chan.id, k_chan_fname, k_chan.notes))

#   TEST!!!
k_erev = -77
#run(channel_files=["C:/Neurosim/K_T.channel.nml"], ivCurve=True, erev=k_erev)

#data = search_neuromldb("Leak", 'channel')

#pas_chan_doc, pas_chan_fname = get_model_from_neuromldb(data[5]['Model_ID'], 'channel')
#pas_chan = pas_chan_doc.ion_channel[0] # select the first ion channel in the nml doc

#print('Channel %s has notes: %s'%(pas_chan.id, pas_chan.notes))

na_chan = pynml.read_neuroml2_file("C:/Neurosim/NaTs.channel.nml")
k_chan = pynml.read_neuroml2_file("C:/Neurosim/K_T.channel.nml")
pas_chan = pynml.read_neuroml2_file("C:/Neurosim/NMLCH001471.channel.nml")

nml_doc = NeuroMLDocument(id="TestCell")

cell = component_factory("Cell", id="novel_cell")
nml_doc.add(cell)

cell.add_segment(prox=[0,0,0,17.841242], 
                 dist=[0,0,0,17.841242], 
                 seg_type='soma')

cell.set_resistivity('0.03 kohm_cm')
cell.set_init_memb_potential('-65mV')
cell.set_specific_capacitance('1.0 uF_per_cm2')
cell.set_spike_thresh('0mV')


cell.add_channel_density(nml_doc,
                        cd_id='%s_chans'%na_chan.id,
                        ion_channel=na_chan.id,
                        cond_density='150 mS_per_cm2',
                        ion_chan_def_file='NaTs.channel.nml',
                        erev="%s mV"%na_erev)

cell.add_channel_density(nml_doc,
                        cd_id='%s_chans'%k_chan.id,
                        ion_channel=k_chan.id,
                        cond_density='36 mS_per_cm2',
                        ion_chan_def_file='K_T.channel.nml',
                        erev="%s mV"%k_erev)

cell.add_channel_density(nml_doc,
                        cd_id='%s_chans'%pas_chan.id,
                        ion_channel=pas_chan.id,
                        cond_density='0.3 mS_per_cm2',
                        ion_chan_def_file='NMLCH001471.channel.nml',
                        erev="-65 mV")



cell_file = "%s.cell.nml"%nml_doc.id
writers.NeuroMLWriter.write(nml_doc, cell_file)


print("Written cell file to: " + cell_file)

#from neuroml.utils import validate_neuroml2

#validate_neuroml2(cell_file)

#!cat TestCell.cell.nml



