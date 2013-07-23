#!/bin/bash
rm -f expense.db
sqlite3 expense.db < tbl.sql
