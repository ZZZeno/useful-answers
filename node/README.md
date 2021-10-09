### typescript中引用node_modules下的依赖

https://qiita.com/EBIHARA_kenji/items/31b7c1c62426bdabd263

下载包的方式
```bash
npm install [@scope/]package-name[@tag] --save
```

### npm和yarn的区别

https://www.sitepoint.com/yarn-vs-npm/

To avoid package version mismatches, an exact installed version is pinned down in a package lock file. Every time a module is added, npm and Yarn create (or update) a package-lock.json and yarn.lock file respectively. This way, you can guarantee another machine installs the exact same package, while still having a range of allowed versions defined in package.json.

package.json相当于go.mod，package-lock.json或者yarn.lock相当于go.sum，具体用yarn还是npm可以看一下项目里的lock文件是哪个
