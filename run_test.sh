#!/bin/bash
cd /root/promptABtesting
/root/promptABtesting/venv/bin/python neo_test.py \
  --prompt-a "You are a helpful assistant. Answer concisely: {input}" \
  --prompt-b "You are an expert assistant. Provide a detailed answer to: {input}" \
  --dataset customer_support \
  --output ./results/test_report.html