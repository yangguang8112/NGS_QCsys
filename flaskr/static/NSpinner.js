/**
 * 手机端进度展示，样式依赖于“spinner.css”
 */
 function NSpinner() {
}
/**
 * 进度展示容器
 */
NSpinner.container;

/**
 * 显示进度展示，若进度存在（之前创建过），直接显示出来，不存在就先创建再显示
 * 
 */
NSpinner.show = function() {
	if (!NSpinner.container) {
		var mainCon = document.createElement("div");
		mainCon.className = "spinner_continaer";
		// 创建容器
		var spiContainer = document.createElement("div");
		spiContainer.className = "spinner";
		// 创建进度1
		var spiRect1 = document.createElement("div");
		spiRect1.className = "dot white";
		// 创建进度2
		var spiRect2 = document.createElement("div");
		spiRect2.className = "dot";
		// 创建进度3
		var spiRect3 = document.createElement("div");
		spiRect3.className = "dot";
		// 创建进度4
		var spiRect4 = document.createElement("div");
		spiRect4.className = "dot";
		// 创建进度5
		var spiRect5 = document.createElement("div");
		spiRect5.className = "dot";
		// 添加进度
		spiContainer.appendChild(spiRect1);
		spiContainer.appendChild(spiRect2);
		spiContainer.appendChild(spiRect3);
		spiContainer.appendChild(spiRect4);
		spiContainer.appendChild(spiRect5);

		mainCon.appendChild(spiContainer);

		NSpinner.container = mainCon;
		// 将创建好的进度条添加到body中
		document.getElementsByTagName("body")[0].appendChild(mainCon);
	} else {
		NSpinner.container.style.display = "block";
	}
};
/**
 * 隐藏进度展示
 */
NSpinner.hide = function() {
	NSpinner.container.style.display = "none";
};