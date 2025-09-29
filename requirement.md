# Github Star Rank

## 功能说明

Github 仓库 Star 排名功能，根据仓库的 Star 数量对仓库进行排名。功能完全利用 Github 仓库+Action 完成，排名每 2 小时进行一次刷新，结果可以部署到 Github Page。

1. 参与排名的仓库需要在 `repos.txt` 文件中进行配置，每个仓库占一行，格式为 `owner/repo`。
2. 支持给仓库添加 Tags，每个仓库可以添加多个 Tags，每个 Tag 占一行，格式为 `tag`。
3. 排名结果会在 `index.html` 文件中进行展示，每个仓库会展示描述， Star 数量和 Tags。并且支持按照 Tags 进行筛选。

## 部署说明

1.  fork 本项目到自己的仓库。
2.  在自己的仓库 Settings 中开启 Actions。
3.  在自己的仓库 Settings 中开启 Pages，选择 `gh-pages` 分支。
4.  等待 Action 运行完成，刷新 Pages 页面，即可看到排名结果。
