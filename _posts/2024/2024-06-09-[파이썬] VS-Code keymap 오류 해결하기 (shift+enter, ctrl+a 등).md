---
title: "[파이썬] VS-Code keymap 오류 해결하기 (shift+enter, ctrl+a 등)"
date: "2024-06-09"
tags:
  - "Jupyter"
  - "python"
  - "vscode"
  - "환경"
year: "2024"
---

# [파이썬] VS-Code keymap 오류 해결하기 (shift+enter, ctrl+a 등)

원본 게시글: https://velog.io/@euisuk-chung/꿀팁-vs-code-keymapping-오류해결하기-shiftenter-ctrlenter-등



안녕하세요🤗! 오늘은 제가 VS-Code를 사용하면서 자주 겪는 문제인 key-mapping 문제와 이를 해결하는 방법에 대해 다뤄보겠습니다.

VS-Code는 다양한 프로그래밍 언어를 지원하는 강력한 에디터입니다. 하지만 다양한 단축키가 지원되다 보니, 충돌이 발생하기도 합니다. 특히 데이터 과학자나 분석가로서 주피터 노트북을 많이 사용하는 경우, 특정 단축키가 먹통이 되는 문제를 자주 경험합니다.

![VSCode](https://code.visualstudio.com/assets/docs/getstarted/keybinding/keyboard-shortcuts.gif)  

Source: <https://code.visualstudio.com/docs/getstarted/keybindings>

이번 포스팅에서는 이러한 keymapping (또는 keybinding) 문제를 해결하는 두 가지 방법을 소개하겠습니다.

1. Extension 설치로 해결하기
---------------------

가장 간단한 방법은 VSCode 마켓플레이스에서 제공하는 확장 프로그램(Extension)을 설치하는 것입니다.

![extension](https://velog.velcdn.com/images/euisuk-chung/post/afac8f07-b46b-4d0d-aeef-d95445dc484c/image.png)

다양한 keymap 확장 프로그램(Extension)들이 마켓플레이스에서 제공되고 있으며, 저의 경우 주피터노트북에서 문제가 발생하였으므로 Jupyter Keymap을 설치하도록 하겠습니다.

![keymap](https://velog.velcdn.com/images/euisuk-chung/post/c9b1a4e5-1c46-44c4-949d-cf22fdcec4bb/image.png)  

Source: <https://code.visualstudio.com/docs/getstarted/keybindings>

확장 프로그램을 설치하면 대다수의 keymapping 문제가 해결되지만, 때로는 설치한 패키지 간 충돌로 인해 문제가 완전히 해결되지 않을 수 있습니다.

예를 들어, 저의 경우 Shift + Enter는 잘 작동하지만 Ctrl + A가 먹통이 되는 문제가 발생했습니다.

2. 직접 키 바인딩 지정하여 해결하기
---------------------

확장 프로그램 설치로 해결되지 않는 경우, 직접 키 바인딩을 지정하는 방법이 있습니다. 다음 단계를 따라 진행해 보세요.

### 1. Keyboard Shortcuts 설정으로 이동

* **영문 VSCode**: File -> Preferences -> Keyboard Shortcuts
* **한글 VSCode**: 파일 -> 기본 설정 -> 바로가기 키

![VSCODE](https://velog.velcdn.com/images/euisuk-chung/post/7cb2db23-3e03-4161-bc0e-9545b34081a8/image.png)

### 2. Open Keyboard Shortcuts(JSON) 클릭

* **영문 VSCode**: Open Keyboard Shortcuts(JSON)
* **한글 VSCode**: 바로가기 키 열기(JSON)

![JSON](https://velog.velcdn.com/images/euisuk-chung/post/ec8f9788-1fda-438c-92ff-310d81a0b1de/image.png)

### 3. 원하는 단축키 지정 및 저장

아래는 `Shift + Enter`와 `Ctrl + A` 키 바인딩을 설정하는 예시입니다.

```
// 키 바인딩을 이 파일에 넣어서 기본값 재정의
[
    {
        "key": "shift+enter",
        "command": "notebook.cell.executeAndSelectBelow",
        "when": "notebookCellListFocused"
    },
    {
        "key": "ctrl+a",
        "command": "editor.action.selectAll",
        "when": "editorTextFocus && !editorReadonly"
    }
]
```

 **3.1. `Shift + Enter` 키 바인딩 설정**

```
{
    "key": "shift+enter",
    "command": "notebook.cell.executeAndSelectBelow",
    "when": "notebookCellListFocused"
}
```

* **키(`key`)**: `shift+enter`
* **명령어(`command`)**: `notebook.cell.executeAndSelectBelow`
* **조건(`when`)**: `notebookCellListFocused`

📌 **설명**: 이 설정은 `Shift + Enter` 키를 누를 때 실행됩니다.

`notebook.cell.executeAndSelectBelow` 명령어는 현재 주피터 노트북 셀을 실행하고 다음 셀을 선택합니다. 만약 다음 셀이 없다면 새 셀이 생성됩니다. 이 명령어는 노트북 셀 리스트가 포커스된 상태에서만 작동합니다.

 **3.2. `Ctrl + A` 키 바인딩 설정**

```
{
    "key": "ctrl+a",
    "command": "editor.action.selectAll",
    "when": "editorTextFocus && !editorReadonly"
}
```

* **키(`key`)**: `ctrl+a`
* **명령어(`command`)**: `editor.action.selectAll`
* **조건(`when`)**: `editorTextFocus && !editorReadonly`

📌 **설명**: 이 설정은 `Ctrl + A` 키를 누를 때 실행됩니다.

`editor.action.selectAll` 명령어는 현재 텍스트 편집기에서 모든 텍스트를 선택합니다. 이 명령어는 텍스트 편집기가 포커스된 상태이고, 편집기가 읽기 전용이 아닌 경우에만 작동합니다.

마무리
---

이렇게 해서 VSCode에서 발생하는 keymapping 문제를 해결하는 두 가지 방법을 알아보았습니다. 해당 글이 도움이 되셨길 바라며 다음에 또 다른 유용한 팁으로 찾아뵙겠습니다.

오늘도 읽어주셔서 감사합니다! 😊

