from collections.abc import Iterable
from google.cloud import compute_v1
import sys
from typing import Any
from google.api_core.extended_operation import ExtendedOperation
import argparse
import multiprocess as mp
import time


def list_all_instances(
    project_id: str,
) -> dict[str, Iterable[compute_v1.Instance]]:
    
    instance_client = compute_v1.InstancesClient()
    request = compute_v1.AggregatedListInstancesRequest()
    request.project = project_id
    request.max_results = 50

    agg_list = instance_client.aggregated_list(request=request)

    all_instances = []

    for zone, response in agg_list:
        if response.instances:
            for instance in response.instances:
                all_instances.append(instance.name)
    return all_instances


def stop_instance(project_id: str, zone: str, instance_name: str) -> None:

    instance_client = compute_v1.InstancesClient()

    operation = instance_client.stop(
        project=project_id, zone=zone, instance=instance_name
    )
    #wait_for_extended_operation(operation, "instance stopping")


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)
    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


##### Argument Parsing #######
parser = argparse.ArgumentParser(description ='Arguments for stopping all the instances in project')
parser.add_argument('-p', '--project_id',  required = True,  help ='project ID')
args = parser.parse_args()

project_id=args.project_id

instances_list = list_all_instances(project_id)
print("List of all VM instances: " + str(instances_list))

inp = input('Are you sure you want to stop all the VM instances? Please type yes or no: ')

if inp=="yes":
    print("Typed yes, so executing the script")
    num_workers = mp.cpu_count()  
    print(num_workers)
    pool = mp.Pool(num_workers)
    start_time = time.time() 
    for inst in instances_list:
        print(inst)
        pool.apply_async(stop_instance, args = (project_id, "us-central1-a", inst,))
        #stop_instance(project_id, "us-central1-a", inst)
    pool.close()
    pool.join()
    end_time = time.time()
    print("Time taken in parallel processing: "+ str(end_time - start_time))
else:
    print("Typed no, so exiting the script")





