from guizero import App, Picture

app = App(title="guizero grid span example", width=460, height=210, layout="grid")
picture1 = Picture(app, image="YES.jpg", grid=[0,0])
picture2 = Picture(app, image="NO.jpg", grid=[1,0])
picture3 = Picture(app, image="Alert.jpg", grid=[2,0,1,2])
picture4 = Picture(app, image="YES.jpg", grid=[0,1,2,1])

app.display()
