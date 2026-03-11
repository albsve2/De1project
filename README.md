# DE1 Project, Group 1 — NYC Taxi Trip Analysis

Distributed analysis of NYC Yellow Taxi trip data to find the most popular routes per hour of the day. Built on Apache Spark and HDFS, deployed on an OpenStack cluster.

---

## Project Overview

The pipeline processes X monthly parquet files (2012–2018, X GB) from the NYC TLC dataset. It filters out zero-distance trips, extracts the pickup hour, builds a route string from pickup and dropoff location IDs, and counts trips per route per hour.

---

## Software Stack

| Component | Version |
|---|---|
| OS | Ubuntu 22.04 |
| Java | OpenJDK 17 |
| Python | 3.10 |
| Hadoop | 3.3.6 |
| Spark | 3.5.8 |

---

## Cluster Overview

| Node | Internal IP | Public IP | Role |
|---|---|---|---|
| Master | `<MASTER_IP>` | `<FLOATING_IP>` | Spark Master, HDFS NameNode, Spark Driver |
| Worker-1 | `<WORKER_1_IP>` | — | Spark Worker, HDFS DataNode |
| Worker-2 | `<WORKER_2_IP>` | — | Spark Worker, HDFS DataNode |
| Worker-3 | `<WORKER_3_IP>` | — | Spark Worker, HDFS DataNode |

---

## 1. OpenStack Setup

### 1.1 Create VMs
Create 4 VMs with the following configuration:
- **Flavor:** ssc.medium (2 vCPU, 4 GB RAM, 20 GB ephemeral storage)
- **Image:** Ubuntu 22.04
- **Names:** master, worker-1, worker-2, worker-3

Attach Cinder block volumes for persistent storage:
- Master: 25 GB
- Each worker: 23 GB

### 1.2 Network and Security
Assign a floating IP to the master node only. Workers are kept on the internal network and are only accessible through the master.

Create a custom security group and add the following inbound rules:

| Port | Protocol | Purpose |
|---|---|---|
| 22 | TCP | SSH access |
| 8080 | TCP | Spark Master UI |
| 9870 | TCP | HDFS NameNode UI |
| 4040 | TCP | Active Spark job UI |
| 7077 | TCP | Spark cluster communication |
| 9000 | TCP | HDFS communication |

Add a **self-referential ingress rule** that allows all traffic between nodes in the same security group. This allows the master to communicate freely with all workers on the internal network.

### 1.3 Static Hostname Mapping
On all nodes, add the following to `/etc/hosts` so nodes can address each other by name rather than IP:

```
<MASTER_IP>    master
<WORKER_1_IP>  worker-1
<WORKER_2_IP>  worker-2
<WORKER_3_IP>  worker-3
```

### 1.4 Passwordless SSH
Spark and Hadoop need to SSH from the master to the workers without a password in order to start and stop services automatically.

On the master, generate an RSA key pair:
```bash
ssh-keygen -t rsa -b 4096
```

Copy the public key to each worker:
```bash
ssh-copy-id ubuntu@worker-1
ssh-copy-id ubuntu@worker-2
ssh-copy-id ubuntu@worker-3
```

Verify passwordless SSH works:
```bash
ssh ubuntu@worker-1
```

---

## 2. Install Java on All Nodes

Run on master and all workers:
```bash
sudo apt update
sudo apt install -y openjdk-17-jdk
java -version
```

---

## 3. Install Hadoop

Run on master and all workers:
```bash
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz
sudo mv hadoop-3.3.6 /opt/hadoop
```

Add to `~/.bashrc` on all nodes:
```bash
export HADOOP_HOME=/opt/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
```

Configure `/opt/hadoop/etc/hadoop/core-site.xml` on all nodes:
```xml

  
    fs.defaultFS
    hdfs://:9000
  

```

Configure `/opt/hadoop/etc/hadoop/hdfs-site.xml` on all nodes:
```xml

  
    dfs.replication
    2
  
  
    dfs.namenode.name.dir
    /opt/hadoop/data/namenode
  
  
    dfs.datanode.data.dir
    /opt/hadoop/data/datanode
  

```

Set `JAVA_HOME` in `/opt/hadoop/etc/hadoop/hadoop-env.sh` on all nodes:
```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

Add worker hostnames to `/opt/hadoop/etc/hadoop/workers` on the master:
```
worker-1
worker-2
worker-3
```

Format the NameNode (master only, run once):
```bash
hdfs namenode -format -force
```

---

## 4. Install Spark

Run on master and all workers:
```bash
wget https://archive.apache.org/dist/spark/spark-3.5.8/spark-3.5.8-bin-hadoop3.tgz
tar -xzf spark-3.5.8-bin-hadoop3.tgz
sudo mv spark-3.5.8-bin-hadoop3 /opt/spark
```

Add to `~/.bashrc` on all nodes:
```bash
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```

On the master, add to `~/.bashrc`:
```bash
export SPARK_LOCAL_IP=
export SPARK_MASTER_HOST=
export SPARK_SSH_OPTS="-i /path/to/key.pem"
```

On each worker, set `SPARK_LOCAL_IP` to the worker's own IP in `/opt/spark/conf/spark-env.sh`:
```bash
# worker-1
export SPARK_LOCAL_IP=
# worker-2
export SPARK_LOCAL_IP=
# worker-3
export SPARK_LOCAL_IP=
```

Add to `/opt/spark/conf/spark-defaults.conf` on the master:
```
spark.driver.host        <MASTER_IP>
spark.driver.bindAddress <MASTER_IP>
```

Add worker hostnames to `/opt/spark/conf/workers` on the master:
```
worker-1
worker-2
worker-3
```

---

## 5. Start and Stop the Cluster

### Start
```bash
start-dfs.sh
$SPARK_HOME/sbin/start-all.sh
```

### Stop
```bash
$SPARK_HOME/sbin/stop-all.sh
stop-dfs.sh
```

### Verify
```bash
# Should show 3 live DataNodes
hdfs dfsadmin -report

# Open SSH tunnel on your local machine to view Spark UI
ssh -i /path/to/key.pem -L 8080::8080 ubuntu@
# Then open http://localhost:8080 in your browser
```

---

## 6. Running the Job

### Clone the repository
```bash
git clone https://github.com/albsve2/De1project.git
cd De1project
```

### Cluster mode
```bash
spark-submit \
  --master spark://:7077 \
  --conf spark.driver.host= \
  --conf spark.driver.bindAddress= \
  --py-files src/config.py,src/etl_job.py \
  src/analysis_job.py
```

### Local mode (for testing)
Set `MASTER_URL = "local[*]"` in `src/config.py`, then:
```bash
spark-submit \
  --py-files src/config.py,src/etl_job.py \
  src/analysis_job.py
```

---

## 7. Viewing Results

```bash
$SPARK_HOME/bin/pyspark \
  --master spark://:7077 \
  --conf spark.driver.host= \
  --conf spark.driver.bindAddress=
```
```python
df = spark.read.parquet("hdfs:///output/avg_trip_time")
df.show(20)
```

---

## 8. Project Structure

```
De1project/
├── src/
│   ├── config.py         # HDFS paths, Spark settings, cluster IPs
│   ├── etl_job.py        # Load and filter raw parquet files from HDFS
│   └── analysis_job.py   # GroupBy aggregation, writes results to HDFS
├── docs/
│   └── cluster_setup.docx
└── README.md
```

---

## 9. Data

- **Source:** NYC TLC Yellow Taxi Trip Records
- **Location in HDFS:** `hdfs:///data/taxi/*.parquet`
- **Output:** `hdfs:///output/avg_trip_time`

Do not overwrite or delete files in `/data/taxi/`.

---

## 10. Monitoring

| Service | URL |
|---|---|
| Spark Master UI | http://`<FLOATING_IP>`:8080 |
| HDFS NameNode UI | http://`<FLOATING_IP>`:9870 |
| Active Job UI | http://`<FLOATING_IP>`:4040 |

Access requires an open SSH tunnel or direct access to the internal network.

---
