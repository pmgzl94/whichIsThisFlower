import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:camera/camera.dart';
import './seePictures.dart';
import './takePicture.dart';
import './createUser.dart';
// import './login.dart';
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
                flowersPic
              }
          }
      }
  }
""";

class Menu extends StatefulWidget
{
    final String token;
    final CameraDescription camera;

    Menu({Key key,
                  @required this.token,
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
      CreateProfil(token: widget.token),
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
    void dispose()
    {
    // Clean up the controller when the widget is disposed.
      super.dispose();
    }

    @override
    Widget build(BuildContext context) {
      return Scaffold(
        // appBar: AppBar(
        //     title: Text('Menu'),
        //       actions: <Widget>[
        //         IconButton(
        //           icon: Icon(
        //             Icons.photo_camera,
        //             // color: Colors.white,
        //           ),
        //           onPressed: () {
        //             Navigator.push(
        //               context,
        //               MaterialPageRoute(builder: (context) => CreateTakePicture(token: widget.token,
        //                                              camera: widget.camera
        //                   )),
        //             );
        //           },
        //         ),
        //       ],
        //     ),

        body: originalList[tabIndex],//IndexedStack(index: tabIndex, children: listScreens),
        // body: CreateMenuButton(token: widget.token),
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
                    onCompleted: (dynamic resultData) {
                      print("on completed");
                      print(resultData.data);
                    if (resultData != null && resultData.data["getPicture"] != null && resultData.data["getPicture"]["flowersPic"] != null) {
                        print(resultData.data["getPicture"]["flowersPic"]["flowersPic"]);
			var obj = resultData.data["getPicture"]["flowersPic"]["flowersPic"];
   			List<String> resultList = [];
			for (int i = 0; i < obj.length; i++) {
			    resultList.add(obj[i]);
			}
                        print(pics);
                        print(resultList);
                        print("REFRESH");
		      setState(() {
      			  pics = resultList;
    		      });
                    } else {
                      print("coudn't find picture");
                      dialog(context, "image not received");
                      showDialog<AlertDialog>(
                        context: context,
                        builder: (BuildContext context) {
                          return dialog(context, "image not received");
                      });
                    }
                    }
                  ),
                  builder: (RunMutation runMutation, QueryResult result) {
                    return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 16.0),
                        child:                 IconButton(
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
                ),
            );
                  })
              ],
            ),
	    
        body: Column(
          children: <Widget>[
            Expanded(
              child: GridView.count(
                crossAxisCount: 1,
                children: List.generate(pics.length, (index) {
                  return DisplayPictures(name: pics[index]);
                }),
              ),
            )
          ],
        ),
    );
  }
}


class DisplayPictures extends StatefulWidget {
  DisplayPictures({Key key, this.name}) : super(key: key);
  final String name;
  @override
  _DisplayPicturesState createState() => _DisplayPicturesState();
}

class _DisplayPicturesState extends State<DisplayPictures> {
  @override
  initState() {
    _asyncMethod();
    super.initState();
  }

  _asyncMethod() async {
    //comment out the next two lines to prevent the device from getting
    // the image from the web in order to prove that the picture is 
    // coming from the device instead of the web.
    String url = getUri();
    url = url.substring(0, url.length - 7) + "download/" + widget.name;
    print(url);
    var response = await get(url); // <--2
    var documentDirectory = await getApplicationDocumentsDirectory();
    var firstPath = documentDirectory.path + "/images";
    var filePathAndName = documentDirectory.path + '/images/pic.jpg'; 
    //comment out the next three lines to prevent the image from being saved
    //to the device to show that it's coming from the internet
    await Directory(firstPath).create(recursive: true); // <-- 1
    File file2 = new File(filePathAndName);             // <-- 2
    file2.writeAsBytesSync(response.bodyBytes);         // <-- 3
    setState(() {
      imageData = filePathAndName;
      dataLoaded = true;
    });
    dataLoaded = true;
  }

  String imageData;
  bool dataLoaded = false;

  @override
  Widget build(BuildContext context) {
    if (dataLoaded) {
      return Scaffold(
        appBar: AppBar(
          title: Text(widget.name),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Image.file(File(imageData))
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