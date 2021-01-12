/***************************************************************************
**                                                                        **
**  QCustomPlot, an easy to use, modern plotting widget for Qt            **
**  Copyright (C) 2011-2018 Emanuel Eichhammer                            **
**                                                                        **
**  This program is free software: you can redistribute it and/or modify  **
**  it under the terms of the GNU General Public License as published by  **
**  the Free Software Foundation, either version 3 of the License, or     **
**  (at your option) any later version.                                   **
**                                                                        **
**  This program is distributed in the hope that it will be useful,       **
**  but WITHOUT ANY WARRANTY; without even the implied warranty of        **
**  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         **
**  GNU General Public License for more details.                          **
**                                                                        **
**  You should have received a copy of the GNU General Public License     **
**  along with this program.  If not, see http://www.gnu.org/licenses/.   **
**                                                                        **
****************************************************************************
**           Author: Emanuel Eichhammer                                   **
**  Website/Contact: http://www.qcustomplot.com/                          **
**             Date: 25.06.18                                             **
**          Version: 2.0.1                                                **
****************************************************************************/

/************************************************************************************************************
**                                                                                                         **
**  This is the example code for QCustomPlot.                                                              **
**                                                                                                         **
**  It demonstrates basic and some advanced capabilities of the widget. The interesting code is inside     **
**  the "setup(...)Demo" functions of MainWindow.                                                          **
**                                                                                                         **
**  In order to see a demo in action, call the respective "setup(...)Demo" function inside the             **
**  MainWindow constructor. Alternatively you may call setupDemo(i) where i is the index of the demo       **
**  you want (for those, see MainWindow constructor comments). All other functions here are merely a       **
**  way to easily create screenshots of all demos for the website. I.e. a timer is set to successively     **
**  setup all the demos and make a screenshot of the window area and save it in the ./screenshots          **
**  directory.                                                                                             **
**                                                                                                         **
*************************************************************************************************************/

#ifndef _N_QT
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTimer>
#include "qcustomplot.h" // the header file of QCustomPlot. Don't forget to add it to your project, if you use an IDE, so it gets compiled.
#include "Configuration.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
	Q_OBJECT
  
public:
	explicit MainWindow(Configuration *Config_init, QWidget *parent = 0);
	~MainWindow();

	Configuration *Config;
	double SD_max, IC_max, TC_max;
	double SD_min, IC_min, TC_min;
	double IC_0, SD_0;
	int TC_0;
	bool pause_action, run_action;

	void setupDemo(int demoIndex, Configuration *Config);
	void setupRealtimeScatterDemo(QCustomPlot *customPlot, Configuration *Config);
  
public slots:
	void realtimeDataInputSlot(QVector<double> x0, QVector<double> y0,
							   QVector<double> x1, QVector<double> y1,
							   QVector<double> x2, QVector<double> y2,
							   QVector<double> x3, QVector<double> y3,
							   int frame, float R0);
	void setICValue(int IC);
	void setSDValue(int SD);
	void setTCValue(int TC);
	void screenShot();
	void allScreenShots();

signals:
	void arrivedsignal(QVector<double> x0, QVector<double> y0,
					   QVector<double> x1, QVector<double> y1,
					   QVector<double> x2, QVector<double> y2,
					   QVector<double> x3, QVector<double> y3,
					   int frame, float R0);

private:
	Ui::MainWindow *ui;
	QString demoName;
	QTimer dataTimer;
	QCPItemTracer *itemDemoPhaseTracer;
	int currentDemoIndex;

private slots:
	void on_run_button_clicked();
};

#endif // MAINWINDOW_H
#endif // _N_QT
