#python kpi_cdf_parser.py latency 0 400 0 1 0 &
#python kpi_cdf_parser.py maxBufferSize 0 20 0 1 0 &
#python kpi_cdf_parser.py dagRank 0 20000 0 1  0 &
#python kpi_cdf_parser.py dutyCycle 0 0.06 0 1 0 &
#python kpi_cdf_parser.py numNeighbors 0 45 0 1 0 &
#python kpi_cdf_parser.py pdr 0 1 0 1 0

python kpi_full_pdf_parser.py latency 30 90 "steady" "Latency (secs)" 50 &
python kpi_full_pdf_parser.py dutyCycle 30 90 "steady" "Radio duty cycle (%)" 50 &
python kpi_full_pdf_parser.py maxBufferSize 30 90 "steady" "Buffer occupancy (packets)" 50 &
python kpi_full_pdf_parser.py dagRank 30 90 "steady" "DAG Rank" 50 &
python kpi_full_pdf_parser.py numNeighbors 30 90 "steady" "Number of neighbors" 50 &
python kpi_full_pdf_parser.py pdr 30 90 "steady" "PDR (%)" 50

python kpi_full_pdf_parser.py latency 0 90 "all" "Latency (secs)" 50 &
python kpi_full_pdf_parser.py dutyCycle 0 90 "all" "Radio duty cycle (%)" 50 &
python kpi_full_pdf_parser.py maxBufferSize 0 90 "all" "Buffer occupancy (packets)" 50 &
python kpi_full_pdf_parser.py dagRank 0 90 "all" "DAG Rank" 50 &
python kpi_full_pdf_parser.py numNeighbors 0 90 "all" "Number of neighbors" 50 &
python kpi_full_pdf_parser.py pdr 0 90 "all" "PDR (%)" 50

#python kpi_full_cdf_parser.py latency 30 90 "steady" "Latency (secs)" &
#python kpi_full_cdf_parser.py dutyCycle 30 90 "steady" "Radio duty cycle (%)" &
#python kpi_full_cdf_parser.py maxBufferSize 30 90 "steady" "Buffer occupancy (packets)" &
#python kpi_full_cdf_parser.py dagRank 30 90 "steady" "DAG Rank" &
#python kpi_full_cdf_parser.py numNeighbors 30 90 "steady" "Number of neighbors "&
#python kpi_full_cdf_parser.py pdr 30 90 "steady" "PDR (%)"
#
#python kpi_full_cdf_parser.py latency 0 90 "all" "Latency (secs)" &
#python kpi_full_cdf_parser.py dutyCycle 0 90 "all" "Radio duty cycle (%)" &
#python kpi_full_cdf_parser.py maxBufferSize 0 90 "all" "Buffer occupancy (packets)" &
#python kpi_full_cdf_parser.py dagRank 0 90 "all" "DAG Rank" &
#python kpi_full_cdf_parser.py numNeighbors 0 90 "all" "Number of neighbors "&
#python kpi_full_cdf_parser.py pdr 0 90 "all" "PDR (%)"
$SHELL