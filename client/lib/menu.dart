import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:camera/camera.dart';
import './seePictures.dart';
import './takePicture.dart';
import './createUser.dart';
import './login.dart';


final String logout = """
  mutation logout(\$token: String!) {
      logout(token: \$token) {
          ok {
            ... on IsOk {
                ok
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
    // CreateMenuButton(token: widget.token),
    // CreateMenuButton(token: widget.token),
    // CreateMenuButton(token: widget.token),
      CreateMenu(token: widget.token, camera: widget.camera),
      CreateTakePicture(token: widget.token, camera: widget.camera),
      CreateLogin(),
      // Tab1(),
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
                title: Text('Menu'),
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.photo_camera),
                title: Text('Camera'),
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.person),
                title: Text('Profil'),
              ),
            ]),
	    backgroundColor: Theme.of(context).primaryColor,
	    // backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
        // body: Center(child: RawWords()),
      // home: MyHomePage(title: 'Flutter Demeau Home Page'),
    );
  }
}

class CreateMenu extends StatelessWidget
{
    final String token;
    final CameraDescription camera;

    CreateMenu({Key key,
                  @required this.token,
                  @required this.camera,
             }) : super(key: key);

    @override
    Widget build(BuildContext context) {
      return Scaffold(
        appBar: AppBar(
            title: Text('Menu'),
              actions: <Widget>[
                IconButton(
                  icon: Icon(
                    Icons.photo_camera,
                    // color: Colors.white,
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => CreateTakePicture(token: token,
                                                     camera: camera
                          )),
                    );
                  },
                ),
              ],
            ),
        body: Column(
          children: [
            Align (
              alignment: Alignment(0.0, -0.75),
              child: CreateMenuButton(token: token),
            ),
          ]
        ),
        backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
        // body: Center(child: RawWords()),
      // home: MyHomePage(title: 'Flutter Demeau Home Page'),
    );
  }
}

class CreateMenuButton extends StatefulWidget
{
    final String token;
    CreateMenuButton({Key key, @required this.token}) : super(key: key);

    @override
    CreateMenuButtonState createState() => CreateMenuButtonState();
}

class CreateMenuButtonState extends State<CreateMenuButton>
{
    final _id = GlobalKey<FormState>();
    bool state = false;

    void hasClicked()
    {
      this.state = true;
    }

    final mc1 = TextEditingController();
    final mc2 = TextEditingController();

    @override
    void dispose() {
    // Clean up the controller when the widget is disposed.
      mc1.dispose();
      mc2.dispose();
      super.dispose();
    }

    @override
    Widget build(BuildContext context) {
      return Form(
            key: _id,
            child: Column(
              children: <Widget> [
               Mutation(
                  options: MutationOptions(
                    documentNode: gql(logout),
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
                      print("LOGOUT");
                      Navigator.pop(context);
                    }
                  ),
                  builder: (RunMutation runMutation, QueryResult result) {
                    return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 16.0),
                        child: ElevatedButton(
                          onPressed: () async {
                            print("GET TOKENNNNNNN");
                            print(widget.token);
                            print("GET ENDED");
                            runMutation({"token": widget.token});
                          },
                          child: Text('Logout'),
                        )
                    );
                  }
                )
              ]
            )
          );
    }
}
