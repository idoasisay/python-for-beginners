from programmers import get_jobs as get_pro_jobs
from stackoverflow import get_jobs as get_so_jobs
from save import save_to_file

programmers_jobs = get_pro_jobs()
stackoverflow_jobs = get_so_jobs()
jobs = programmers_jobs + stackoverflow_jobs

save_to_file(jobs)