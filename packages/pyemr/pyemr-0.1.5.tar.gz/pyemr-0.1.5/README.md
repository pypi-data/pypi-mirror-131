<br><br>


<img src='.media/logo.png' style='width:400px; float:left'>
<br>

# PYEMR : 
<br><br>

## Python EMR Toolkit


A command line tool for developing, testing and packaging pyspark applications on EMR.

<br> 

Install using
```pip install pyemr ```.

<p align="center">
<img src='.media/code.png' style='width:350px;'>
</p>

### Features: 

- Easily submit Spark scripts along with any dependencies via venv
- Shortcuts for viewing logs, ssm and canceling steps 
- Launch Amazon Linux notebooks/bash locally


<br>
<br>

# Usage

## 1. Submit Package

1. Init the project config [toml](https://python-poetry.org/).  Specify a target cluster and stage directory,
```
pyemr init \
--project_name=example \
--target_cluster="Cluster Name" \
--s3_stage_dir=s3://some/s3/directory \
--stage=dev \
--region=eu-west-1
```

Add your code and dependencies.

2.  Then build and push the package to s3, 
```
pyemr build 
```
(NOTE: The first time you run this its building the docker image from scratch. This might take > 5 min.)

3. Submit to the cluster, 
```
pyemr submit src/script.py --arg 1
```



<br>
<br>

## 2. Debugging 

### logs

Download and print stdout/stderror of last step (when using client mode),

```
pyemr stdout 
```

Or a specific step
```
pyemr stderror --step_id <step_id>
```

Download logs
```
pyemr download_logs ./logs
```

### ssm

ssm into the master node,
```
pyemr ssm 
```

Or the master of another cluster, 
```
pyemr ssm <cluster_name>
```


### ls

List steps,
```
pyemr list_steps
```

List clusters, 
```
pyemr list_clusters
```

### cancel 

Cancel last step submited by the project, 
```
pyemr cancel_step
```

Cancel last step submited by the project,
```
pyemr cancel_step <step_id>
```

<br>
<br>

## 3. Local 

Run a script locally in Amazon Linux docker, 
```
pyemr test src/script.py
```

Start a Python Notebook running in an Amazon Linux Docker container, 
```
pyemr notebook
```

Start an Amazon linux bash/sh session with current directory mounted,
```
pyemr bash
```

Start a local interactive python/pyspark session in Amazon Linux,
```
pyemr pyspark
```


### 4. TODO: Export
Export as airflow step,
```
pyemr export src/script.py -o airflow_script.py
```

<br> 
<br> 
<br> 
<br> 

------------------------------------------------------

<br> 
<br> 
<br> 
<br> 
<br> 


## Appendix
<br>

### Dependencies
Requires docker.

### Development 

To reformat the code run 
```
python pyemr/utils/dev.py 
```

Lint code,
```
pylint **/*.py
```

<br> 

### Troubleshoot

#### 1. 
```
[Errno 28] No space left on device
```

#### Solution: 

```
docker system prune
```

WARNING! This will remove:
- all stopped containers
- all networks not used by at least one container
- all dangling images
- all dangling build cache


<br><br>

####  1.

```
botocore.exceptions.ClientError: An error occurred (InvalidSignatureException) when calling the ListClusters operation: Signature expired: 20211210T145000Z is now earlier than 20211210T145057Z (20211210T145557Z - 5 min.)
```


#### Solution

https://stackoverflow.com/questions/61640295/aws-invalidsignatureexception-signature-expired-when-running-from-docker-contai



### TODO 
- Add airflow code generator 


