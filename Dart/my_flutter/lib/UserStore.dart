import 'package:get/state_manager.dart';

class UserStore extends GetxController {
  RxMap<dynamic, dynamic> userInfo = {}.obs;

  void setUserInfo(Map<String, dynamic> info) {
    userInfo.value = info;
  }
}
