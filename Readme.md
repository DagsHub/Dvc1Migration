# DVC 0 to DVC 1 Migration Script
Want to ask a quick question? Join our community [![Discord](https://img.shields.io/discord/698874030052212737)](https://discord.com/invite/9gU36Y6)  !

This script was provided by dagshub, and powered by the the following [gist](https://gist.githubusercontent.com/skshetry/07a3e26e6b06783e1ad7a4b6db6479da/raw/919786bf6dd5c97dbb64a53c5066de3bb2f5e57d/migrator.py)

### The fast way – Spare me the details!

I recommend that you carry on reading to take a look at what the script is actually doing, but if you absolutely just want to run the script you can do the following

```bash
curl 'https://raw.githubusercontent.com/DAGsHub/Dvc1Migration/master/migrator.py' -O \
&& curl 'https://raw.githubusercontent.com/DAGsHub/Dvc1Migration/master/migrate.sh' -O \
&& chmod +x migrate.sh && ./migrate.sh
```

### The long way – I want to understand!

Download [this python script](https://gist.github.com/skshetry/07a3e26e6b06783e1ad7a4b6db6479da) provided by one of DVC's collaborators and copy it to the working directory

```bash
curl https://gist.githubusercontent.com/skshetry/07a3e26e6b06783e1ad7a4b6db6479da/raw/919786bf6dd5c97dbb64a53c5066de3bb2f5e57d/migrator.py -O
```

The scripts requires you to have the `argparse` package in your python environment

```bash
pip install argparse
```

Now the script provided takes as arguments an original .dvc file (or Dvcfile) and the name of the stage as it should appear in our pipeline. 

This means you have to manually run `python [migrate.py](http://migrate.py) <file.dvc> <stage_name>` numerous time. When it comes to a pipeline with many stages, this might become cumbersome. Moreover, some of the .dvc files don't represent stages in your pipeline but just tracked files cache information. These should not appear as stages in your `dvc.yaml` file. 

Let's write a bash script that takes care of that

```bash
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
```

You can download it like this

```bash
curl 'https://raw.githubusercontent.com/DAGsHub/Dvc1Migration/master/migrate.sh' -O
```

**What is `migrate()` actually doing?**

In short it will search for .dvc files that have a "cmd" key, and add their content as stages in the new format. For example if you currently have a stage file named `train.dvc`, the script will assume you want to call the stage `train`. Feel free to alter this behaviour to your liking! 

All the original .dvc files will be backed up as `<old_file>.dvc.bak` and two new files will be created at the root of your working directory:

1. [dvc.yaml](https://dvc.org/doc/user-guide/dvc-files-and-directories#dvcyaml-file)
2. [dvc.lock](https://dvc.org/doc/user-guide/dvc-files-and-directories#dvclock-file)

To run the command just make it executable

```bash
chmod +x migrate.sh
```

And run it!

```bash
./migrate.sh
```

Start tracking the newly generated files by running

```bash
git stage -u .
git add dvc.yaml dvc.lock
git commit -m "migration to dvc 1"
git push -u origin dvc-1-migration
```


---

Made with 🐶 by [DAGsHub](https://dagshub.com/).
