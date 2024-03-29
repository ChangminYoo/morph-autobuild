import os
import shutil
import tkinter
import ttkbootstrap
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import webbrowser
from functools import partial

# 포함 되어야 할 폴더 (zipper)
zip_includes = ['/Assets', '/Packages', '/ProjectSettings']

# 이동할 기본 폴더 (OpenStudio)
move_targets = ['com.unity.sharp-zip-lib@1.2.2-preview.2',
                'Ifland AvatarEngine',
                'Ifland AvatarEngine Using ExPlugins',
                'Ifland AvatarOpenEngine',
                'ifland.tra@2.3.52',
                ]

# buildproject 배포위해 만들어지게 될 플랫폼
buildproject_platform = [('Android', True), ('iOS', True), ('WebGL', True), ('Win', True)]
# buildproject에 포함되어야 할 폴더
buildproject_includes = [('Assets', True), ('Packages', True), ('ProjectSettings', True), ('Library', True)]


class ZipBuilder:
    # input 디렉토리 절대경로
    dir0 = 'C:/'
    dir1 = 'C:/'
    # input 디렉토리 리스트
    dir_list = [dir0]
    # 산출 상위 폴더 이름
    folder_name = 'Result'
    # 산출 절대경로
    out_dir = 'C:/' + folder_name
    # input에서 각 산출될 이름을 저장
    dir_dictionary = {}

    move_to = 'Packages'

    def __init__(self):
        self.dir_count = 0
        self.label_text = []  # zip path text list
        self.entry_list = []  # mover entry list - target folder to move

        self.windowWidth = 450
        self.windowHeight = 500

        # window
        self.window = ttk.Window("AOP", themename='cosmo')
        self.window.geometry("{}x{}+500+300".format(self.windowWidth, self.windowHeight))

        # text
        self.curr_path = os.getcwd()
        self.move_input_text = tkinter.StringVar(value=self.curr_path)
        self.move_output_text = tkinter.StringVar(value=self.curr_path)
        self.mover_result_folder = tkinter.StringVar(value='IflandOpenStudio')
        self.out_text = tkinter.StringVar(value=self.out_dir)  # zip output path text
        self.build_input_text = tkinter.StringVar(value=self.curr_path)  # buildproject input
        self.build_output_text = tkinter.StringVar(value=self.curr_path)  # buildproject output
        self.build_result_folder = tkinter.StringVar(value='Unity_BuildProject')

        # notebook
        notebook = ttk.Notebook(self.window, width=self.windowWidth, height=self.windowHeight)
        notebook.pack()
        self.frame_openstudio = ttk.Frame(self.window)
        notebook.add(self.frame_openstudio, text='OpenStudio')
        self.frame_buildproject = ttk.Frame(self.window)
        notebook.add(self.frame_buildproject, text='BuildProject')
        self.frame_zip = ttk.Frame(self.window)
        notebook.add(self.frame_zip, text='Zipper')

        # set Zipper
        for directory in self.dir_list:
            self.dir_dictionary[directory] = self.make_out_name(directory)
        self.set_zipper_gui()

        # set open studio
        for target in move_targets:
            name = tkinter.StringVar()
            name.set(target)
            self.entry_list.append(name)
        self.set_openstudio_gui()

        # set build project
        self.set_buildproject_gui()

        self.window.mainloop()

    def exist_path(self, directory):
        if os.path.isdir(directory):
            return True
        else:
            print("Not Exist ::: ", directory)
            return False

    def show_done_message(self, path):
        tkinter.messagebox.showinfo('완료', '완료 했습니다.')
        self.window.destroy()
        self.window.quit()
        webbrowser.open(path)

    # region Zipper
    def set_zipper_frame(self):
        ttk.Label(self.frame_zip, text="디렉토리를 변경할 수 있습니다.").pack()

        input_frame = ttk.LabelFrame(self.frame_zip, text="Input", padding=(20, 10))
        input_frame.place(x=15, y=40, width=self.windowWidth - 30, height=210)

        output_frame = ttk.LabelFrame(self.frame_zip, text='Output')
        output_frame.place(x=15, y=280, width=self.windowWidth - 30, height=70)

    def set_zipper_gui(self):
        self.set_zipper_frame()

        for i in range(0, len(self.dir_list)):
            self.label_text.append(tkinter.StringVar())
            self.label_text[i].set(self.dir_list[i])

        for i in range(0, len(self.dir_list)):
            dir_label = ttk.Label(self.frame_zip, textvariable=self.label_text[i], width=45,
                                  relief='sunken', anchor=tkinter.CENTER)
            dir_label.place(x=100, y=70 * (i + 1))
            dir_button = ttk.Button(self.frame_zip, text='Path', style='Accent.TButton', width=5,
                                    command=partial(self.open_dir_zip, i, True))
            dir_button.place(x=30, y=65 * (i + 1))

        ttk.Button(self.frame_zip, text='+', width=5, command=self.add_zipper_button).place(x=370, y=252)

        out_label = ttk.Label(self.frame_zip, textvariable=self.out_text, width=40,
                              relief='sunken', anchor=tkinter.CENTER)
        out_label.place(x=130, y=312)
        output_button = ttk.Button(self.frame_zip, text='Output', width=8, style='Accent.TButton',
                                   command=partial(self.open_dir_zip, 0, False))
        output_button.place(x=28, y=307)

        start_button = ttk.Button(self.frame_zip, text='Start', width=25, command=self.make_zip)
        start_button.place(x=120, y=365)

    def add_zipper_button(self):
        index = len(self.dir_list)
        if index >= 3:
            return

        self.dir_list.append('C:/')
        self.label_text.append(tkinter.StringVar())
        self.label_text[index].set(self.dir_list[index])

        dir_label = ttk.Label(self.frame_zip, textvariable=self.label_text[index], width=45, relief='sunken',
                              anchor=tkinter.CENTER)
        dir_label.place(x=100, y=67 * (index + 1))
        dir_button = ttk.Button(self.frame_zip, text='Path', style='Accent.TButton', width=5,
                                command=partial(self.open_dir_zip, index, True))
        dir_button.place(x=30, y=65 * (index + 1))
        self.dir_dictionary[self.dir_list[index]] = self.make_out_name(self.dir_list[index])

    def open_dir_zip(self, num, is_input):
        dir_name = filedialog.askdirectory(parent=self.window, initialdir=self.curr_path, title='폴더를 선택해 주세요')
        print('Select : ', dir_name)

        if is_input:
            if self.dir_list[num] in self.dir_dictionary:
                self.dir_dictionary.pop(self.dir_list[num])
            self.dir_dictionary[dir_name] = self.make_out_name(dir_name)
            self.dir_list[num] = dir_name
            self.label_text[num].set(dir_name)
        else:
            self.out_dir = dir_name
            self.out_text.set(dir_name + '/' + self.folder_name)
            for directory in self.dir_dictionary:
                self.dir_dictionary[directory] = self.make_out_name(directory)

    def make_out_name(self, st):
        string = st.split('/')
        return self.out_dir + '/' + self.folder_name + '/' + string[len(string) - 1]

    def make_zip(self):
        print('------------ START -------------')
        # includes 내에 속한 폴더만 복사
        for directory in self.dir_dictionary:
            for folder in zip_includes:
                if self.exist_path(directory + folder):
                    shutil.copytree(directory + folder, self.dir_dictionary[directory] + folder, dirs_exist_ok=True)
                    print("From : ", directory + folder,
                          "    =====>    Copy To : ", self.dir_dictionary[directory] + folder)
        # zip 변환
        print("Zipping................")
        for out in self.dir_dictionary:
            filename = self.dir_dictionary[out]
            os.chdir(self.out_dir)
            if self.exist_path(out):
                shutil.make_archive(filename, 'zip', filename)
        print('------------ FINISH -------------')
        self.show_done_message(self.out_dir)

    # endregion

    # region OpenStudio
    def set_openstudio_gui(self):
        # Input
        input_frame = ttk.LabelFrame(self.frame_openstudio, text='Input')
        input_frame.place(x=20, y=5, width=self.windowWidth - 40, height=60)
        input_label = tkinter.Entry(self.frame_openstudio, textvariable=self.move_input_text,
                                    relief='sunken', width=45, justify=ttk.CENTER)
        input_label.place(x=100, y=30)
        input_button = ttk.Button(self.frame_openstudio, text='Path', style='Accent.TButton',
                                  width=5, command=partial(self.open_dir_openstudio, True))
        input_button.place(x=30, y=25)

        # Output
        output_frame = ttk.LabelFrame(self.frame_openstudio, text='Output')
        output_frame.place(x=20, y=70, width=self.windowWidth - 40, height=60)
        output_label = tkinter.Entry(self.frame_openstudio, textvariable=self.move_output_text,
                                     relief='sunken', width=45, justify=ttk.CENTER)
        output_label.place(x=100, y=95)
        output_button = ttk.Button(self.frame_openstudio, text='Path', style='Accent.TButton',
                                   width=5, command=partial(self.open_dir_openstudio, False))
        output_button.place(x=30, y=90)

        # Folder List
        list_frame = ttk.LabelFrame(self.frame_openstudio, text='Folder List', labelanchor='n')
        list_frame.place(x=40, y=145, width=self.windowWidth - 80, height=210)
        for i in range(0, len(self.entry_list)):
            entry = ttk.Entry(self.frame_openstudio, textvariable=self.entry_list[i], width=40)
            entry.place(x=80, y=170 + (i * 35))

        # ttk.Button(self.frame_openstudio, text='+', width=3, command=self.add_mover_button).place(x=360, y=370)

        ttk.Entry(self.frame_openstudio, textvariable=self.mover_result_folder, width=20).place(x=140, y=370)
        move_button = ttk.Button(self.frame_openstudio, text='Start', width=25, command=self.move_folder)
        move_button.place(x=120, y=425)

    def add_mover_button(self):
        index = len(self.entry_list)
        if index >= 6:
            return

        self.entry_list.append(tkinter.StringVar())
        self.entry_list[index].set('')

        entry = ttk.Entry(self.frame_openstudio, textvariable=self.entry_list[index], width=40)
        entry.place(x=80, y=135 + (index * 35))

    def open_dir_openstudio(self, is_input):
        dir_name = filedialog.askdirectory(parent=self.window, initialdir=self.curr_path, title='폴더를 선택해 주세요')
        if is_input:
            self.move_input_text.set(dir_name)
        else:
            self.move_output_text.set(dir_name)

    def move_folder(self):
        print('------------ Move -------------')
        to = self.move_input_text.get() + '/' + self.move_to
        output = self.move_output_text.get() + '/' + self.mover_result_folder.get()
        if not self.exist_path(self.move_input_text.get()) or not self.exist_path(self.move_output_text.get()):
            print('Path Error')
            return

        if self.move_input_text.get() == self.move_output_text.get():
            for folder in self.entry_list:
                if not folder.get() == '':
                    move = self.move_input_text.get() + '/Assets/' + folder.get()
                    if self.exist_path(move):
                        # input과 output이 같은 경로일 경우에는 이동만
                        shutil.move(move, to)
        else:
            for folder in zip_includes:
                shutil.copytree(self.move_input_text.get() + folder, output + folder, dirs_exist_ok=True)
            self.delete_metafile()
            to = output + '/' + self.move_to
            for folder in self.entry_list:
                if not folder.get() == '':
                    move = output + '/Assets/' + folder.get()
                    if self.exist_path(move):
                        shutil.move(move, to)
        print('------------  FINISH  ------------ ')
        self.show_done_message(output)

    def delete_metafile(self):
        path = self.move_output_text.get() + '/' + self.mover_result_folder.get() + '/Assets'
        for file in os.listdir(path):
            if file.endswith('.meta'):
                os.remove(os.path.join(path, file))

    # endregion

    # region BuildProject
    def set_buildproject_gui(self):
        # Input
        input_frame = ttk.LabelFrame(self.frame_buildproject, text='Input')
        input_frame.place(x=20, y=10, width=self.windowWidth - 40, height=70)
        input_label = tkinter.Entry(self.frame_buildproject, textvariable=self.build_input_text,
                                    relief='sunken', width=45, justify=ttk.CENTER)
        input_label.place(x=100, y=40)
        input_button = ttk.Button(self.frame_buildproject, text='Path', style='Accent.TButton',
                                  width=5, command=partial(self.open_dir_buildproject, True))
        input_button.place(x=30, y=35)

        # Output
        output_frame = ttk.LabelFrame(self.frame_buildproject, text='Output')
        output_frame.place(x=20, y=90, width=self.windowWidth - 40, height=70)
        output_frame = tkinter.Entry(self.frame_buildproject, textvariable=self.build_output_text,
                                     relief='sunken', width=45, justify=ttk.CENTER)
        output_frame.place(x=100, y=120)
        output_button = ttk.Button(self.frame_buildproject, text='Path', style='Accent.TButton',
                                   width=5, command=partial(self.open_dir_buildproject, False))
        output_button.place(x=30, y=115)

        # include
        buildproject_include_frame = ttk.LabelFrame(self.frame_buildproject, text='Include')
        buildproject_include_frame.place(x=50, y=180, width=130, height=180)
        for i in range(0, len(buildproject_includes)):
            check = tkinter.Checkbutton(self.frame_buildproject, text=buildproject_includes[i][0],
                                        font=('맑은 고딕', 10, 'bold'), command=partial(self.change_include_value, i))
            check.select()
            check.place(x=55, y=210 + (i * 35))

        # platform
        buildproject_platform_frame = ttk.LabelFrame(self.frame_buildproject, text='Platform')
        buildproject_platform_frame.place(x=260, y=180, width=130, height=180)
        for i in range(0, len(buildproject_platform)):
            check = tkinter.Checkbutton(self.frame_buildproject, text=buildproject_platform[i][0],
                                        font=('맑은 고딕', 10, 'bold'),
                                        command=partial(self.change_platform_value, i))
            check.select()
            check.place(x=265, y=210 + (i * 35))

        ttk.Entry(self.frame_buildproject, textvariable=self.build_result_folder, width=20).place(x=140, y=375)

        move_button = ttk.Button(self.frame_buildproject, text='Start', width=25, command=self.buildproject_move)
        move_button.place(x=120, y=425)

    def change_platform_value(self, i):
        if buildproject_platform[i][1]:
            buildproject_platform[i] = (buildproject_platform[i][0], False)
        else:
            buildproject_platform[i] = (buildproject_platform[i][0], True)

    def change_include_value(self, i):
        if buildproject_includes[i][1]:
            buildproject_includes[i] = (buildproject_includes[i][0], False)
        else:
            buildproject_includes[i] = (buildproject_includes[i][0], True)

    def open_dir_buildproject(self, is_input):
        dir_name = filedialog.askdirectory(parent=self.window, initialdir=self.curr_path, title='폴더를 선택해 주세요')
        if is_input:
            self.build_input_text.set(dir_name)
        else:
            self.build_output_text.set(dir_name)

    def buildproject_move(self):
        check_right_folder = False
        move = self.build_input_text.get()
        to = self.build_output_text.get() + '/' + self.build_result_folder.get()
        for i in range(0, len(buildproject_includes)):
            move = self.build_input_text.get() + '/' + buildproject_includes[i][0]
            if self.exist_path(move):
                if buildproject_includes[i][1]:
                    for j in range(0, len(buildproject_platform)):
                        if buildproject_platform[j][1]:
                            folder = to + '/' + buildproject_platform[j][0] + '/' + buildproject_includes[i][0]
                            shutil.copytree(move, folder, dirs_exist_ok=True)
                            print("Move ==== ", move, " -----> ", folder)
                            check_right_folder = True

        split_path = self.build_input_text.get().split('/')
        move_path = ''
        for s in range(0, len(split_path) - 1):
            move_path += split_path[s]
            move_path += '/'

        guide_txt = move_path + 'Document/Guide.txt'
        guid_docx = move_path + 'Document/OpenPlatform Build Guide.docx'
        build_sh = move_path + 'Unity_BuildProject/build.sh'
        costume_test_folder = move_path + 'CostumeResourcesForTest'

        if check_right_folder:
            if os.path.exists(guide_txt):
                shutil.copy(guide_txt, to)
            if os.path.exists(guid_docx):
                shutil.copy(guid_docx, to)
            if os.path.exists(build_sh):
                shutil.copy(build_sh, to)
            if os.path.exists(costume_test_folder):
                shutil.copytree(costume_test_folder, to + '/CostumeResourcesForTest', dirs_exist_ok=True)
            self.show_done_message(to)
        else:
            print("Input은 AOP : BuildProject_DLL, COP : build_project 폴더를 선택해 주세요")

    # endregion


if __name__ == '__main__':
    ZipBuilder()
