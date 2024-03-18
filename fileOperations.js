

import React, { useState } from 'react';
import { StyleSheet, View, TextInput, Button, Text } from 'react-native';
import * as FileSystem from 'expo-file-system';
import { StorageAccessFramework } from 'expo-file-system';
import * as DocumentPicker from 'expo-document-picker';

export default function App() {
  const [fileName, setFileName] = useState('');
  const [fileContent, setFileContent] = useState('');
  const [message, setMessage] = useState('');


  const createAndWriteFile = async () => {
    try {
      const permissions = await StorageAccessFramework.requestDirectoryPermissionsAsync();
      if (permissions.granted) {
        let directoryUri = permissions.directoryUri;
        const fileUri = await StorageAccessFramework.createFileAsync(
          directoryUri,
          `${fileName}.csv`,
          "text/csv",
        );
        await FileSystem.writeAsStringAsync(fileUri, fileContent);
        setMessage('File created and content written successfully');
      } else {
        setMessage('Permission to access directory denied');
      }
    } catch (error) {
      console.log(error)
      setMessage('Error creating file or writing content');
    }
  };

  const readFile = async () => {
    try {
      const document = await DocumentPicker.getDocumentAsync({ type: '*/*' });
  
      if (document.assets.length === 1) {
        console.log(document);
        console.log(document.assets[0].uri);
        const content = await FileSystem.readAsStringAsync(document.assets[0].uri);
        setFileName(document.assets[0].name);
        setFileContent(content);
        setMessage('File content retrieved successfully');
      } else {
        setMessage('No file selected');
      }
    } catch (error) {
      setMessage('Error reading file');
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="File name"
        value={fileName}
        onChangeText={setFileName}
      />
      <TextInput
        style={styles.input}
        placeholder="File content"
        multiline
        numberOfLines={4}
        value={fileContent}
        onChangeText={setFileContent}
      />
      <Button title="Create File & Write Content" onPress={createAndWriteFile} />
      <Button title="Read File" onPress={readFile} />
      <Text style={styles.message}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 10,
  },
  input: {
    marginBottom: 10,
    padding: 10,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 4,
  },
  message: {
    marginTop: 10,
    color: 'red',
  },
});
