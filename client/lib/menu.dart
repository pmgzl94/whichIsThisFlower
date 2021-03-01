import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:camera/camera.dart';
import './seePictures.dart';
import './takePicture.dart';
import './createUser.dart';
import './profil.dart';
import './client.dart';
import 'package:http/http.dart' show get;
import 'dart:io';
import 'package:path_provider/path_provider.dart';


final String getPicture = """
  mutation getPicture(\$token: String!) {
      getPicture(token: \$token) {
          ok {
            ... on IsOk {
                ok
              }
          },
          flowersPic {
            ... on GetFlowersPic {
                flowersPic,
                flowersName
              }
          }
      }
  }
""";

class Menu extends StatefulWidget
{
    final String token;
    final String username;
    final CameraDescription camera;

    Menu({Key key,
                  @required this.token,
                  @required this.username,
                  @required this.camera,
             }) : super(key: key);


    @override
    MenuState createState() => MenuState();
}

class MenuState extends State<Menu>
{
    List<Widget> originalList;
    Map<int, bool> originalDic;
    List<Widget> listScreens;
    List<int> listScreensIndex;
    int tabIndex = 1;

    Widget men;
    List<Widget> listMen;


    @override
    void initState() {
      super.initState();
      originalList = [
        // CreateMenu(token: widget.token, camera: widget.camera),
        CreateMyObs(token: widget.token),
        CreateTakePicture(token: widget.token, camera: widget.camera),
        CreateProfil(token: widget.token, username: widget.username),
      ];
      originalDic = {0: false, 1: true, 2: false};
      listScreens = [originalList[1]];
      listScreensIndex = [1];
    }

    void _selectedTab(int index) {
        if (originalDic[index] == false) {
          listScreensIndex.add(index);
          originalDic[index] = true;
          listScreensIndex.sort();
          listScreens = listScreensIndex.map((index) {
            return originalList[index];
          }).toList();
        }

        setState(() {
          tabIndex = index;
        });
    }


    @override
    void dispose() {
    // Clean up the controller when the widget is disposed.
      super.dispose();
    }

    @override
    Widget build(BuildContext context) {
      return Scaffold(
        body: originalList[tabIndex],//IndexedStack(index: tabIndex, children: listScreens),
        bottomNavigationBar: BottomNavigationBar(
            currentIndex: tabIndex,
            onTap: _selectedTab,
            items: [
              BottomNavigationBarItem(
                icon: Icon(Icons.home),
                title: Text('Observation'),
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.photo_camera),
                title: Text('Camera'),
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.person),
                title: Text('Profile'),
              ),
            ]),
            backgroundColor: Colors.white,
            // backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
    );
  }
}

class CreateMyObs extends StatefulWidget
{
    final String token;
    CreateMyObs({Key key, this.token}) : super(key: key);
    @override
    MyObsState createState() => new MyObsState();
}

class MyObsState extends State<CreateMyObs>
{
    List<String> pics = [];
    List<String> flowerNames = [];
    List<String> imageData = [];
    bool dataLoaded = false;


    @override
    void dispose() {
    // Clean up the controller when the widget is disposed.
        super.dispose();
    }

    @override
    void initState() {
      super.initState();
    }


    @override
    Widget build(BuildContext context) {
      return Scaffold(
        appBar: AppBar(
              title: Text('My observations'),
              centerTitle: true,
              automaticallyImplyLeading: false,
              actions: <Widget>[
                Mutation(
                    options: MutationOptions(
                      documentNode: gql(getPicture),
                      update: (Cache cache, QueryResult result) {
                        return cache;
                      },
                      onError: (result) {
                        print("error");
                        print(result);
                      },
                      onCompleted: (dynamic resultData) async {
                        print("on completed");
                        print(resultData.data);
                        if (resultData != null && resultData.data["getPicture"] != null && resultData.data["getPicture"]["flowersPic"] != null) {
                            print(resultData.data["getPicture"]["flowersPic"]["flowersPic"]);
                            var obj = resultData.data["getPicture"]["flowersPic"]["flowersPic"];
                            var obj2 = resultData.data["getPicture"]["flowersPic"]["flowersName"];
                            List<String> resultList = [];
                            List<String> names = [];
                            for (int i = 0; i < obj.length; i++) {
                                resultList.add(obj[i]);
                                names.add(obj2[i]);
                            }
                            print(pics);
                            print(resultList);
                            print("REFRESH");
                            setState(() {
                                pics = resultList;
                                flowerNames = names;
                            });
                            String url = getUri();
                            url = url.substring(0, url.length - 7) + "download/";

                            var documentDirectory = await getApplicationDocumentsDirectory();
                            var firstPath = documentDirectory.path + "/images";
                            await Directory(firstPath).create(recursive: true);

                            List<String> filepaths = [];
                            for (var i = 0; i < pics.length; i++) {
                              var response = await get(url + pics[i]);
                              var filePathAndName = documentDirectory.path + '/images/${pics[i]}.jpg';
                              File file2 = new File(filePathAndName);
                              file2.writeAsBytesSync(response.bodyBytes);
                              filepaths.add(filePathAndName);
                            }
                            setState(() {
                              imageData = filepaths;
                              // dataLoaded = true;
                            });
                            print("done!!");
                            dataLoaded = true;
                        } else {
                          print("coudn't find pictures");
                          dialog(context, "images not received");
                          showDialog<AlertDialog>(
                            context: context,
                            builder: (BuildContext context) {
                              return dialog(context, "images not received");
                            }
                          );
                        }
                      }
                    ),
                    builder: (RunMutation runMutation, QueryResult result) {
                      return IconButton(
                        icon: Icon(
                          Icons.refresh_outlined,
                          color: Colors.black,
                        ),
                        onPressed: () async {
                          print("GET TOKENNNNNNN");
                          print(widget.token);
                          print("GET ENDED");
                          runMutation({"token": widget.token});
                          print("PRESSED");
                        },
                      );
                    })
              ],
        ),
      //  DisplayPictures2(names: pics)
              body: dataLoaded ? ListView.builder(
          // padding: const EdgeInsets.all(8),
          itemCount: pics.length,
          itemBuilder: (BuildContext context, int index) {
            return Padding(
              padding: EdgeInsets.all(20),
              child: Column(
                children: <Widget>[
                  Text(flowerNames[index]),
                  // Image.network("https://i.imgur.com/xl0jdfS.jpg"),
                  Image.file(File(imageData[index]))
                ],
              ),
            );
          }
        )
        : CircularProgressIndicator(
          backgroundColor: Colors.cyan,
          strokeWidth: 5,
        )
      );
    }
}

class DisplayPictures extends StatefulWidget
{
    final String name;
    DisplayPictures({Key key, this.name}) : super(key: key);

    @override
    _DisplayPicturesState createState() => _DisplayPicturesState();
}

class _DisplayPicturesState extends State<DisplayPictures>
{
    String imageData;
    bool dataLoaded = false;

    @override
    initState() {
      _asyncMethod();
      super.initState();
    }

    _asyncMethod() async {
      String url = getUri();
      url = url.substring(0, url.length - 7) + "download/" + widget.name;
      print(url);
      var response = await get(url);
      var documentDirectory = await getApplicationDocumentsDirectory();
      var firstPath = documentDirectory.path + "/images";
      var filePathAndName = documentDirectory.path + '/images/pic.jpg';
      await Directory(firstPath).create(recursive: true);
      File file2 = new File(filePathAndName);
      file2.writeAsBytesSync(response.bodyBytes);
      setState(() {
        imageData = filePathAndName;
        dataLoaded = true;
      });
      dataLoaded = true;
    }

    @override
    Widget build(BuildContext context) {
      if (dataLoaded) {
          return Scaffold(
              resizeToAvoidBottomPadding: false,
              body: new Container(
                  alignment: Alignment.center,
                  margin: EdgeInsets.only(left: 40.0, right: 40.0),
                  // padding: EdgeInsets.all(30),
                  decoration: new BoxDecoration(
                  // color: Colors.black, //Color.fromRGBO(0, 180, 0, 0.6),
                  borderRadius: new BorderRadius.only(
                        topLeft:  const  Radius.circular(40.0),
                        topRight: const  Radius.circular(40.0),
                        bottomLeft:  const  Radius.circular(40.0),
                        bottomRight: const  Radius.circular(40.0)
                  )
              ),
              child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Image.file(File(imageData)),
                    Padding(
                        padding: EdgeInsets.only(top: 10.0),
                        child: new Text(
                          widget.name,
                          style: TextStyle(
                              fontSize: 18.0,
                              fontWeight: FontWeight.bold,
                              // color: Colors.white
                          ),
                        ),
                    )
              ],
            ),
          ),
        );
      } else {
        return CircularProgressIndicator(
          backgroundColor: Colors.cyan,
          strokeWidth: 5,
        );
      }
    }
}