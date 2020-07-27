<div align="center">
  <a href="https://dagshub.com"><img src="https://raw.githubusercontent.com/DAGsHub/client/master/dagshub_github.png" width=600 alt=""/></a><br><br>
</div>

[![Discord](https://img.shields.io/discord/698874030052212737)](https://discord.com/invite/9gU36Y6)

# DVC 0 to DVC 1 Migration Script
This script was provided by DAGsHub, and based on the the following [gist](https://gist.githubusercontent.com/skshetry/07a3e26e6b06783e1ad7a4b6db6479da/raw/919786bf6dd5c97dbb64a53c5066de3bb2f5e57d/migrator.py) provided by one of [DVC](https://github.com/iterative/dvc)'s collaborators.

### The fast way – Spare me the details!

I recommend that you carry on reading to take a look at what the script is actually doing, but if you absolutely just want to run the script you can do the following

```bash
curl 'https://raw.githubusercontent.com/DAGsHub/Dvc1Migration/master/migrator.py' | python -
```

### The long way – I want to understand!

In DVC ≤ 0.94 stages were named after the files containing their details — `Dvcfile` or `<name>.dvc`. Since DVC 1 you define the name of the stage and not the name of the file containing it.

[This python script](https://gist.github.com/skshetry/07a3e26e6b06783e1ad7a4b6db6479da) provided by one of DVC’s collaborators is converting a single-stage file into a stage inside `dvc.yaml` and `dvc.lock`. It takes as arguments an original `.dvc` file (or `Dvcfile`) and the name of the stage as it should appear in our new pipeline. This means you have to manually run `python migrator.py <file.dvc> <stage_name>` numerous times. When it comes to a pipeline with many stages, this might become cumbersome. Moreover, some of the `.dvc` files don't represent stages in your pipeline but just tracked files cache information. This means they were created by DVC when running the command `dvc add` or `dvc import`. These should not appear as stages in your dvc.yaml file.

I took the liberty to alter the script so that it could migrate an entire project with as many `.dvc` files as I want. In short, it will search for `.dvc` files that have a "cmd" key, and add their content as a stage in the new format. For example, if you currently have a stage file named `train.dvc`, the script will assume you want to call the stage `train`. Feel free to alter this behavior to your liking!

You can download it like this:
```bash
curl 'https://raw.githubusercontent.com/DAGsHub/Dvc1Migration/master/migrator.py' -O
```

All the original `.dvc` files will be backed up as `<old_file>.dvc.bak` and two new files will be created at the root of your working directory
1. [dvc.yaml](https://dvc.org/doc/user-guide/dvc-files-and-directories#dvcyaml-file)
2. [dvc.lock](https://dvc.org/doc/user-guide/dvc-files-and-directories#dvclock-file)

To run the command:
```bash
python migrator.py
```

The output should look like this:
```bash
Creating 'dvc.yaml'
Adding stage 'featurization' in 'dvc.yaml'
Generating lock file 'dvc.lock'
Adding stage 'training' in 'dvc.yaml'
Updating lock file 'dvc.lock'
Adding stage 'Dvcfile' in 'dvc.yaml'
Updating lock file 'dvc.lock'
...
```

If you don’t recognize this pattern, feel free to describe your problem in the comments below and I’ll do my best to take a look at it.

Otherwise, start tracking the newly generated files by running:
```bash
git stage -u .
git add dvc.yaml dvc.lock
git commit -m "migration to dvc 1"
git push -u origin dvc-1-migration
```

This will:
1. Mark the old `.dvc` files as deleted in git, while keeping the backup files in your working directory untracked
2. Add the new `dvc.yaml` and `dvc.lock` to you git tree
3. Commit and push the branch `dvc-1-migration` to your `origin` remote

That’s it, you have now migrated your project to DVC 1!

---

Made with 🐶 by [DAGsHub](https://dagshub.com/).
