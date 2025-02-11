import logging
import os
from pathlib import Path

import enoslib as en

# en.init_logging(level=logging.INFO)
# en.check()

ip_address=[]

# Set very high parallelism to be able to handle a large number of VMs
en.set_config(ansible_forks=1)

# Enable Ansible pipelining
os.environ["ANSIBLE_PIPELINING"] = "True"

job_name = Path(__file__).name
# change walltime for longer or shoter reserve time.
# change cluster for different cluster in grid5000
# change number for more VMs
# change flavour_desc for setting different CPU and Memory of VMs

conf = en.VMonG5kConf.from_settings(job_name=job_name, walltime="02:00:00",image="/grid5000/virt-images/debian11-x64-min.qcow2").add_machine(
    roles=["fog"],
    cluster="ecotype",
    number=1,
    flavour_desc={"core": 4, "mem": 8192},
)

provider = en.VMonG5k(conf)

#Get actual resources
roles, networks = provider.init()

# Wait for VMs to finish booting
en.wait_for(roles)

# Run same command on all VMs
results = en.run_command("uname -a", roles=roles)
for result in results:
    print(result.payload["stdout"])
	
ip_address.append(roles["fog"][0].address)

f = open("node_list", 'a')
f.write(str(ip_address[0]))
f.write("\n")
f.close
    
#provider.destroy()