mkdir -p taxi_data

for year in $(seq 2012 2018)
do
  for month in $(seq -w 1 12)
  do
    url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_${year}-${month}.parquet"
    wget -nc -P ~/taxi_data --user-agent="Mozilla/5.0" --tries=10 --waitretry=2 --timeout=30 --wait=2 --random-wait --limit-rate=1m --referer="https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page" "$url" || true
  done
done
