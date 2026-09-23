# Third-Party Notices

AMC-Drive is released as a Drive-JEPA-lineage NAVSIM v1 proposal planner. This
file records the main upstream systems, code families, and research projects
that AMC-Drive depends on or acknowledges.

| Project | Source | Used component | License / notice |
| --- | --- | --- | --- |
| Drive-JEPA | https://github.com/linhanwang/Drive-JEPA | Proposal-based driving planner, training/evaluation conventions, NAVSIM integration pattern | Apache-2.0 repository license; cite Drive-JEPA |
| NAVSIM | https://github.com/autonomousvision/navsim | Dataset/devkit, scenario loading, PDM/NAVSIM evaluation conventions | NAVSIM license and citation required |
| nuPlan / nuPlan-devkit | https://github.com/motional/nuplan-devkit | Map, actor-state, trajectory, simulation, and metric utilities | nuPlan license and citation required |
| V-JEPA 2 | https://github.com/facebookresearch/vjepa2 | Predictive representation context in the Drive-JEPA lineage | Upstream license and citation required |
| BEVFormer | https://github.com/fundamentalvision/BEVFormer | BEV transformer design lineage used by the planner stack | Upstream license and citation required |
| MMCV | https://github.com/open-mmlab/mmcv | Transformer and deformable attention utilities | Apache-2.0 |
| MMDetection | https://github.com/open-mmlab/mmdetection | Detection/model utility dependency | Apache-2.0 |
| TransFuser | https://github.com/autonomousvision/transfuser | End-to-end driving architecture context and loss lineage | Upstream license and citation required |
| Bench2Drive | https://github.com/Thinklab-SJTU/Bench2Drive | Driving benchmark context and score-module lineage | Upstream license and citation required |
| Hugging Face Hub | https://huggingface.co | V1 checkpoint distribution | Hugging Face terms apply |

This notice is not a substitute for the upstream licenses. Users are
responsible for checking all dataset, checkpoint, benchmark, and software
license requirements before redistribution or commercial use.
