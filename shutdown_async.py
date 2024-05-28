from collections.abc import Iterable
from google.cloud import compute_v1
import sys
from typing import Any
from google.api_core.extended_operation import ExtendedOperation
import argparse
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor


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
    print(instance_name)
    instance_client = compute_v1.InstancesClient()

    operation = instance_client.stop(
        project=project_id, zone=zone, instance=instance_name
    )
    #await wait_for_extended_operation(operation, "instance stopping")


async def wait_for_extended_operation(
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

async def waiter(instances_list,project_id,zone):
    print("Entered waiter")
    tasks=[]
    for inst in instances_list:
        t=asyncio.create_task(stop_instance(project_id, zone, inst))
        tasks.append(t)
    for i in range(len(tasks)):
        await tasks[i]
    #asyncio.gather(*tasks)

# #@asyncio.coroutine
# def main(instances_list,project_id, zone):
#     for inst in instances_list:
#         yield from loop.run_in_executor(p, stop_instance, 5)

##### Argument Parsing #######
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description ='Arguments for stopping all the instances in project')
    parser.add_argument('-p', '--project_id',  default="cmetestproj", help ='project ID')
    parser.add_argument('-z', '--zone', help ='project ID', default="us-central1-a")
    args = parser.parse_args()

    project_id=args.project_id
    zone=args.zone

    instances_list = list_all_instances(project_id)
    print("List of all VM instances: " + str(instances_list))

    inp = input('Are you sure you want to stop all the VM instances? Please type yes or no: ')

    if inp=="yes":
        print("Typed yes, so executing the script")
        #loop = asyncio.get_event_loop()
        #p = ThreadPoolExecutor(max_workers=40)
        #loop.run_until_complete(main(instances_list,project_id, zone))
        #group = asyncio.gather(*[stop_instance(project_id, zone, inst) for inst in instances_list])
        #group_task = asyncio.create_task(*[stop_instance(project_id, zone, inst) for inst in instances_list])
        start_time = time.time() 
        #with ThreadPoolExecutor(max_workers=40) as executor:
            #future = executor.map(stop_instance, project_id, zone, instances_list)
            #print(future.result())
        # for inst in instances_list:
        #     print(inst)
        #     asyncio.run(stop_instance(project_id, zone, inst))
        #await group_task
        #results = loop.run_until_complete(group)
        #asyncio.run(waiter(instances_list,project_id, zone))
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(stop_instance, project_id, zone, inst): inst for inst in instances_list}


        end_time = time.time()
        print("Time taken in parallel processing: "+ str(end_time - start_time))
    else:
        print("Typed no, so exiting the script")





