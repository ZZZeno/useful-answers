### typescript中引用node_modules下的依赖

https://qiita.com/EBIHARA_kenji/items/31b7c1c62426bdabd263

下载包的方式
```bash
npm install [@scope/]package-name[@tag] --save
```

### npm和yarn的区别

https://www.sitepoint.com/yarn-vs-npm/

To avoid package version mismatches, an exact installed version is pinned down in a package lock file. Every time a module is added, npm and Yarn create (or update) a package-lock.json and yarn.lock file respectively. This way, you can guarantee another machine installs the exact same package, while still having a range of allowed versions defined in package.json.

`package.json` 相当于`go.mod`，`package-lock.json`或者`yarn.lock`相当于`go.sum`，具体用`yarn`还是`npm`可以看一下项目里的lock文件是哪个


### mongoose 语句加 `.exec()` 和不加的区别
如果调用的地方加await的话在执行上没有任何区别，但是在出现异常的时候，加了.exec()之后返回的堆栈信息会更有用一点

https://stackoverflow.com/a/68469848/6060776
