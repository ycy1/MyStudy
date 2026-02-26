import 'package:flutter/material.dart';

class SnackBarUtil {
  static ScaffoldFeatureController showSnackBar(
    BuildContext context,
    String message, {
    Duration duration = const Duration(seconds: 3),
  }) {
    return ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        width: 100,
        behavior: SnackBarBehavior.floating,
        backgroundColor: Colors.blueAccent,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        duration: duration,
        content: Text(message, textAlign: TextAlign.center),
      ),
    );
  }

  static ScaffoldFeatureController showErrorSnackBar(
    BuildContext context,
    String message, {
    Duration duration = const Duration(seconds: 3),
  }) {
    return ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        width: 100,
        behavior: SnackBarBehavior.floating,
        backgroundColor: Colors.red,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        duration: duration,
        content: Text(message, textAlign: TextAlign.center),
      ),
    );
  }

  static ScaffoldFeatureController showWarningSnackBar(
    BuildContext context,
    String message, {
    Duration duration = const Duration(seconds: 3),
    double width = 100,
  }) {
    return ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        width: width,
        behavior: SnackBarBehavior.floating,
        backgroundColor: const Color.fromARGB(255, 195, 135, 24),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        duration: duration,
        content: Text(message, textAlign: TextAlign.center),
      ),
    );
  }
}
