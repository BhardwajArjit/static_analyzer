import 'dart:io';
import 'dart:convert';
import 'dart:math';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:crypto/crypto.dart';

void main() {
  // Insecure File Permissions Example
  File file = File('sensitive_data.txt');
  file.writeAsStringSync('Sensitive Data');

  // Rooted Device Access Simulation (Pseudo-code)
  // Note: In Flutter, detecting rooted devices requires platform-specific code, so this is a placeholder for illustration.
  print('Accessing device with ID: ROOTED_DEVICE_ID');

  // Lack of Hashing Example
  String data = 'password123';
  var bytes = utf8.encode(data);
  var digest = md5.convert(bytes);
  print('MD5 hash: ${digest.toString()}');

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Flutter Security Example'),
        ),
        body: Center(
          child: Text('Security vulnerabilities demo'),
        ),
      ),
    );
  }
}
