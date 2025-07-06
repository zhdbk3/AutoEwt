# AutoEwt

## 协议与声明

- 本软件遵循 [GNU General Public License v3.0](LICENSE) 开源许可证。
- **本软件的目的仅在研究 `Python` 技术，您不得使用它来应付学校的任务，或是做其他违反纪律、法律的事。**
- **如果您擅自使用本软件做不当的事，产生的任何后果和影响均由您自己承担，与我们无关。**
- **开始使用本软件即代表您同意上述协议和声明，同意 [着火的冰块nya](https://space.bilibili.com/551409211)
  及其他开发者不为您的行为承担任何责任。**

## 如何使用

### 1. 下载浏览器驱动

请打开您的浏览器，查看它的版本。

然后下载**对应版本**的浏览器驱动，解压后放在您喜欢的位置。

以下是一些您可能用得到的链接：

- [Chrome 驱动文件下载 (chromedriver)](https://www.cnblogs.com/aiyablog/articles/17948703)
- [Edge 驱动文件下载 (msedgedriver)](https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver)
- [Firefox 驱动文件下载 (geckodriver)](https://github.com/mozilla/geckodriver/releases)

以下是所有**可能**支持的浏览器：

- Firefox
- Chrome
- Ie
- Edge
- Safari
- WebKitGTK
- WPEWebKit

推荐使用 **Edge**，因为我们的开发就在 Edge 上进行。别的浏览器不保证能用。

### 2. 修改配置文件

请根据您自己的情况，修改 `config.yml.default` 中的内容，并删去 `.default` 后缀：

```yaml
# 修改时不要删掉冒号后的空格
browser: 浏览器名称（首字母大写），如 Chrome, Edge 等
driver_path: 浏览器驱动路径
username: 用户名
password: 密码
list_url: 课程列表页面的链接
```

### 3. 启动！

双击运行 `AutoEwt`，然后用您的双手去做更有意义的事！

## 开发环境

- Python 3.12
- Edge 138
