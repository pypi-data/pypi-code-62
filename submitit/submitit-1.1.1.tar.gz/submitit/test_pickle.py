# import submitit
# import torch.multiprocessing as mp


# def work(rank):
#     print("Test!", rank)


# def test():
#     ps = []
#     mp.set_start_method("spawn")
#     for rank in [0, 1]:
#         p = mp.Process(target=work, args=(rank,))
#         p.start()
#         ps.append(p)
#     for p in ps:
#         p.join()


# if __name__ == "__main__":
#     # executor = submitit.AutoExecutor(folder="log")
#     # executor.update_parameters(timeout_min=5, slurm_partition="learnfair", nodes=1, cpus_per_task=1, slurm_constraint="pascal")
#     # job = executor.submit(test)
#     # output = job.result()

#     test()
