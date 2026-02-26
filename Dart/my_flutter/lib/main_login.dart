import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widget_previews.dart';
import 'package:get/get.dart';
import 'package:my_flutter/UserStore.dart';
import 'DioUtil.dart';
import 'SnackBarUtil.dart';

void main(List<String> args) {
  runApp(LoginPage());
}

class LoginPage extends StatefulWidget {
  @Preview(size: Size(300, 800))
  const LoginPage({super.key});

  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    debugPrint('createState');
    return _LoginPageState();
  }
}

class _LoginPageState extends State<LoginPage> {
  late DioUtil? dioUtil;
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final controller = Get.put(UserStore());

  final UserStore _userStore = Get.find();
  String errorMsg = '';
  @override
  void initState() {
    // TODO: implement initState
    dioUtil = DioUtil();
    super.initState();
    debugPrint('initState');
  }

  @override
  Widget build(BuildContext context) {
    dioUtil = dioUtil ?? DioUtil();
    // TODO: implement build
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Login')),
        body: Form(
          key: _formKey,
          child: Container(
            padding: EdgeInsets.all(16),
            child: Column(
              children: [
                TextFormField(
                  controller: _usernameController,
                  decoration: InputDecoration(labelText: '用户名'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      errorMsg = '请输入用户名';
                      return '请输入用户名';
                    }
                    RegExp regExp = RegExp(r'^[a-zA-Z0-9_]+$');
                    if (!regExp.hasMatch(value)) {
                      errorMsg = '用户名只能包含字母、数字和下划线';
                      return '用户名只能包含字母、数字和下划线';
                    }

                    return null;
                  },
                ),
                SizedBox(height: 15),
                TextFormField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: InputDecoration(labelText: '密码'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      errorMsg = '请输入密码';
                      return '请输入密码';
                    }
                    return null;
                  },
                ),
                SizedBox(height: 15),
                Builder(
                  builder: (localContext) {
                    return TextButton(
                      onPressed: () async {
                        // 验证表单
                        // Form.of(localContext)!.validate()
                        if (_formKey.currentState!.validate()) {
                          // 登录
                          var password = _passwordController.text;
                          var username = _usernameController.text;
                          debugPrint(
                            'username: $username, password: $password',
                          );
                          // var response = await dioUtil!.get<String>(
                          //   'https://www.baidu.com',
                          // );
                          // debugPrint(response.toString());
                          debugPrint('登录');
                          // controller.obs.userInfo.value = {
                          //   'username': username,
                          //   'password': password,
                          // };
                          _userStore.setUserInfo({
                            'username': username,
                            'password': password,
                          });
                          SnackBarUtil.showSnackBar(localContext, '登录成功');
                        } else {
                          debugPrint('登录失败');
                          SnackBarUtil.showWarningSnackBar(
                            localContext,
                            '登录失败\n$errorMsg',
                            width: 200,
                          );
                        }
                      },
                      child: Text("登录"),
                    );
                  },
                ),

                Obx(() {
                  return Text('${_userStore.userInfo.value['username'] ?? ''}');
                }),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
