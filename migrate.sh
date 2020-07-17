#!/bin/bash

migrate() {
	for file_path in $(find . -type f -name "*.dvc" && find . -type f -name "Dvcfile")
	do
		# check if the file has a top level "cmd" key
		if grep -q "^ *cmd:" ${file_path} ; then
			# replace a stage file <stage_name>.dvc to <stage_name>
			stage_name="$(basename ${file_path} .dvc)"
			echo "migrating ${file_path} as stage \"${stage_name}\""
			python migrator.py ${file_path} ${stage_name}
		fi
	done
}

migrate