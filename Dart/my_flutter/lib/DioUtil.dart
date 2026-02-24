import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

class DioUtil {
  final _dio = Dio();
  DioUtil() {
    _dio.options..baseUrl = 'http://127.0.0.1:8800'
    ..connectTimeout = const Duration(seconds: 5)
    ..receiveTimeout = const Duration(seconds: 5)
    ..sendTimeout = const Duration(seconds: 5);
    
    addInterceptors();
  }

  void addInterceptors() {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        // Do something before request is sent
        return handler.next(options); //continue
        // If you want to resolve the request with some custom data，
        // you can resolve a `Response` object eg: `handler.resolve(response)`.
        // If you want to reject the request with a error message,
        // you can reject a `DioError` object eg: `handler.reject(dioError)`
      },
      onResponse: (response, handler) {
        // Do something with response data
        // debugPrint('response: ${response}');
        // debugPrint(response.toString());
        debugPrint(response.statusCode.toString());
        debugPrint(response.toString());
        if (response.statusCode != 200) {
          // Do something with response data
          return handler.reject(DioException(
            requestOptions: response.requestOptions,
            response: response,
            type: DioExceptionType.badResponse, 
            message: response.statusMessage,
          ));
        }
        return handler.next(response); // continue
        // If you want to reject the request with a error message,
        // you can reject a `DioError` object eg: `handler.reject(dioError)`
      },
      onError: (DioException e, handler) {
        // Do something with response error
        return handler.reject(e);
        // return handler.next(e); //continue
        // If you want to resolve the request with some custom data，
        // you can resolve a `Response` object eg: `handler.resolve(response)`.
      }
    )); 
  }

  Future<Response> get(String url, {Map<String, dynamic>? queryParameters}) async {
    try {
      Response response = await _dio.get(url, queryParameters: queryParameters);
      return response;
    } on DioException catch (e) {
      throw e;
    }
  }

}