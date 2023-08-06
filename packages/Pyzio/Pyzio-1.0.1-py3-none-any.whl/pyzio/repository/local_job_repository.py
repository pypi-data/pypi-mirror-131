from queue import PriorityQueue
from typing import List, Tuple, Optional

from ..domain.job import Job
from ..pyzio_logger import PyzioLogger


class LocalJobRepository:
    def __init__(self, logger: PyzioLogger):
        self._logger = logger
        self._job_q = PriorityQueue()

    def update_jobs(self, jobs: List[Job]) -> None:
        while not self._job_q.empty():
            self._job_q.get()
        for job in jobs:
            entry = job.sequence_number, job.part_id, job.job_id, job.filename, \
                    job.printFile, job.cluster_id, job.team_id
            self._job_q.put((job.sequence_number, entry))

    def peek_job_from_queue(self) -> Job:
        sequence_number, part_id, job_id, filename, print_file, cluster_id, team_id = self._job_q.queue[0][1]
        return Job(sequence_number, part_id, job_id, filename, cluster_id, team_id, print_file)

    def get_job_from_queue(self) -> Job:
        sequence_number, part_id, job_id, filename, print_file, cluster_id, team_id = self._job_q.get()[1]
        return Job(sequence_number, part_id, job_id, filename, cluster_id, team_id, print_file)

    def get_job_by_id(self, id: str) -> Optional[Job]:
        for sequence_number, entry in self._job_q.queue:
            sequence_number, part_id, job_id, filename, print_file, cluster_id, team_id = entry
            if job_id == id:
                return Job(sequence_number, part_id, job_id, filename, cluster_id, team_id, print_file)
        return None

    def is_queue_empty(self):
        return self._job_q.empty()
