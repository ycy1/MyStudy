# WebP 无损图片
WebP 是一种新型图片格式，可为网络上的图片提供品质卓越的无损和有损压缩。使用 WebP，网站站长和网络开发者可以创建体积更小但细节更丰富的图片，从而提高网络访问速度。

## 下载并安装 WebP
[webp](https://developers.google.cn/speed/webp/download?hl=zh-cn)
### Windows 
下载解压缩后直接在bin目录下执行命令即可，不在赘述！

### Linux
安装 libjpeg、libpng、libtiff 和 libgif 软件包，以便在 JPEG、PNG、TIFF、GIF 和 WebP 图片格式之间进行转换。

软件包管理因 Linux 发行版而异。在 Ubuntu 和 Debian 上，以下命令将安装所需的软件包：
```
yum -y install libjpeg-dev libpng-dev libtiff-dev libgif-dev
```
解压下载的tar xvzf libwebp-1.5.0.tar.gz
```
cd libwebp-1.5.0
./configure
make
sudo make install
```
这会构建并安装 cwebp 和 dwebp 命令行工具以及 libwebp 库（动态和静态）。

默认情况下，这些工具通常安装在 /usr/local/bin/ 下。本地版本是在 examples/ 目录下构建的。

该库通常会安装在 /usr/local/lib/ 目录下。为避免运行时错误，请确保您的 LD_LIBRARY_PATH 环境变量包含此位置。C 头文件通常安装在 /usr/local/include/webp 下。

### 使用
使用 cwebp 将图片转换为 WebP 格式
在命令行中使用 cwebp 将 PNG 或 JPEG 图片文件转换为 WebP 格式。您可以将 PNG 图片文件转换为具有质量范围的 WebP 图片 （共 80 个）：

```
cwebp [options] input_file -o output_file.webp
```
常用选项

- ***-o string***
指定输出 WebP 文件的名称。如果省略，cwebp 将执行 压缩，但只报告统计信息。 使用“-”作为输出名称将会将输出定向到“stdout”。

- ***-q float***
指定 RGB 通道的压缩系数，介于 0 和 100 之间。默认值为 75。
如果是有损压缩（默认），较小的系数会产生较小的 质量较低的文件使用值 100 可实现最佳画质。

- ***-z int***
开启 lossless 压缩模式，并指定级别（介于 0 到 9 之间），其中级别 0 表示最快，级别 9 表示最慢。与速度较慢的模式相比，快速模式生成的文件大小更大。建议采用 -z 6 作为默认值。 此选项实际上是质量和方法的一些预定义设置的快捷方式。如果随后使用选项 -q 或 -m，它们将使此选项失效。

- ***-mt***
如有可能，请使用多线程进行编码。

其他选项见官网  [cwebp](https://developers.google.cn/speed/webp/docs/cwebp?hl=zh-cn)

### 上栗子🌰
**结合Java**
```java
/**
     * 压缩文件并返回压缩后的文件
     * @param multipartFile 文件
     * @return 压缩后的文件
     */
public static File compressFile(MultipartFile multipartFile) {
        log.info("libwebp：文件压缩start,大小:{}", FileUtils.convertFileSize(multipartFile.getSize()));
        String outputPath = System.getProperty("user.dir") + File.separator + "libwebp";
        try {
            String filePath = outputPath + File.separator + multipartFile.getOriginalFilename();
            // 创建临时文件
            File file = new File(filePath);
            // 将 MultipartFile 内容传输到文件
            multipartFile.transferTo(file);
            String LIBWEBP_HOME = System.getenv("LIBWEBP_HOME");
            String cmd = "cwebp.exe -q 50 -mt " + filePath + " -o " + outputPath + File.separator + "compressFile.webp";
            // 创建一个ProcessBuilder实例
            ProcessBuilder builder = new ProcessBuilder("cmd", "/c", LIBWEBP_HOME + cmd); // 使用dir命令列出当前目录的内容
            builder.redirectErrorStream(true); // 将错误输出和标准输出合并
            // 启动进程
            Process process = builder.start();

            // 读取命令的输出（如果有的话）
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "GBK"));
            String line;
            while ((line = reader.readLine()) != null) {
                log.info("libwebp：{}", line);
            }
            // 等待进程结束
            int exitCode = process.waitFor();
            FileUtil.del(file);
//            System.out.println("Exited with code: " + exitCode);
//            System.exit(0);

        } catch (Exception e) {
            log.error("文件压缩异常,{}", e.getMessage());
        }
        File compressFile = new File(outputPath + File.separator + "compressFile.webp");
        log.info("libwebp：文件压缩end,大小:{}", FileUtils.convertFileSize(compressFile.length()));
        return compressFile;
    }
```
![image.png](http://182.92.85.80/group1/M00/00/02/tlxVUGh3waiAP-SRAAQ2gk_OtRE144.png)
![image.png](http://182.92.85.80/group1/M00/00/02/tlxVUGh3wgmAFtzuAACHWP4Zv-Q489.png)
![image.png](http://182.92.85.80/group1/M00/00/02/tlxVUGh3whqAG22AAACuoRV4Gvo533.png)

**End**