/*---------------------------------------------------------------------------------*/
/*  COVID SIM - Agent-based model of a pandemic in a population -                  */
/*                                                                                 */
/*  COVID SIM - version 1.0.0 has been created by                                  */
/*                 Khalil Al Handawi           - McGill University                 */
/*                                                                                 */
/*  The copyright of NOMAD - version 3.9.1 is owned by                             */
/*                 Khalil Al Handawi           - McGill University                 */
/*                 Michael Kokkolaras          - McGill University                 */
/*                                                                                 */
/*                                                                                 */
/*  Contact information:                                                           */
/*    McGill University - Systems Optimization Lab (SOL)                           */
/*    Macdonald Engineering Building, 817 Sherbrooke Street West,                  */
/*    Montreal (Quebec) H3A 0C3 Canada                                             */
/*    e-mail: khalil.alhandawi@mail.mcgill.ca                                      */
/*    phone : 1-514-398-2343                                                       */
/*                                                                                 */
/*  This program is free software: you can redistribute it and/or modify it        */
/*  under the terms of the GNU Lesser General Public License as published by       */
/*  the Free Software Foundation, either version 3 of the License, or (at your     */
/*  option) any later version.                                                     */
/*                                                                                 */
/*  This program is distributed in the hope that it will be useful, but WITHOUT    */
/*  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or          */
/*  FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License    */
/*  for more details.                                                              */
/*                                                                                 */
/*  You should have received a copy of the GNU Lesser General Public License       */
/*  along with this program. If not, see <http://www.gnu.org/licenses/>.           */
/*                                                                                 */
/*---------------------------------------------------------------------------------*/

/**
 \file   motion.cpp
 \brief  Methods related to population mobility and related computations (implementation)
 \author Khalil Al Handawi
 \date   2010-08-25
 \see    motion.h
 */

#include "motion.h"

 /*-----------------------------------------------------------*/
 /*                      Update positions                     */
 /*-----------------------------------------------------------*/
Eigen::ArrayXXf update_positions(Eigen::ArrayXXf population, double dt)
{
	/*update positions of all people

	Uses heading and speed to update all positions for
	the next time step

	Keyword arguments
	---------------- -
	population : ndarray
	the array containing all the population information

	dt : float
	Time increment used for incrementing velocity due to forces
	*/

	// update positions
	// x
	population.col(1) += population.col(3) * dt;
	// y
	population.col(2) += population.col(4) * dt;

	return population;
}

/*-----------------------------------------------------------*/
/*                      Update velocities                    */
/*-----------------------------------------------------------*/
Eigen::ArrayXXf update_velocities(Eigen::ArrayXXf population, double max_speed, double dt)
{
	/*update positions of all people

	Uses heading and speed to update all positions for
	the next time step

	Keyword arguments
	---------------- -
	population : ndarray
	the array containing all the population information

	max_speed : float
	Maximum speed cap for individuals

	dt : float
	Time increment used for incrementing velocity due to forces
	*/

	// Apply force
	population.col(3) += population.col(15) * dt;
	population.col(4) += population.col(16) * dt;

	// Limit speed
	Eigen::ArrayXf speed = population(Eigen::all, { 3,4 }).rowwise().norm(); // current distance travelled
	population(select_rows(speed > max_speed), { 3,4 }).colwise() *= max_speed / speed(select_rows(speed > max_speed));

	// Limit force
	population(Eigen::all, { 15,16 }) = 0.0;

	return population;
}

/*-----------------------------------------------------------*/
/*                      Update wall forces                   */
/*-----------------------------------------------------------*/
Eigen::ArrayXXf update_wall_forces(Eigen::ArrayXXf population, Eigen::ArrayXXf xbounds, Eigen::ArrayXXf ybounds,
	double wall_buffer, double bounce_buffer)
{
	/*checks which people are about to go out of bounds and corrects

	Function that calculates wall repulsion forces on individuals that are about to
	go outside of the world boundaries.

	Keyword arguments
	---------------- -
	population : ndarray
	the array containing all the population information

	xbounds, ybounds : list or tuple
	contains the lower and upper bounds of the world[min, max]

	wall_buffer, bounce_buffer : float
	buffer used for wall force calculation and returning
	individuals within bounds
	*/

	int pop_size = population.rows();

	// Avoid walls
	Eigen::ArrayXXf wall_force = Eigen::ArrayXXf::Zero(pop_size, 2);

	Eigen::ArrayXf to_lower_x = population.col(1) - xbounds.col(0);
	Eigen::ArrayXf to_lower_y = population.col(2) - ybounds.col(0);

	Eigen::ArrayXf to_upper_x = xbounds.col(1) - population.col(1);
	Eigen::ArrayXf to_upper_y = ybounds.col(1) - population.col(2);

	// Bounce individuals within the world
	ArrayXXb bounce_lo_x(to_lower_x.rows(), 2), bounce_lo_y(to_lower_x.rows(), 2);
	bounce_lo_x << (to_lower_x > -bounce_buffer), (to_lower_x < 0.0); // , (population.col(3) < 0);
	bounce_lo_y << (to_lower_y > -bounce_buffer), (to_lower_y < 0.0); // , (population.col(4) < 0);

	population(select_rows(bounce_lo_x), { 3 }) = population(select_rows(bounce_lo_x), { 3 }).abs();
	population(select_rows(bounce_lo_y), { 4 }) = population(select_rows(bounce_lo_y), { 4 }).abs();

	population(select_rows(bounce_lo_x), { 1 }) = xbounds(select_rows(bounce_lo_x), { 0 }) + bounce_buffer;
	population(select_rows(bounce_lo_y), { 2 }) = ybounds(select_rows(bounce_lo_y), { 0 }) + bounce_buffer;

	ArrayXXb bounce_ur_x(to_lower_x.rows(), 2), bounce_ur_y(to_lower_x.rows(), 2);
	bounce_ur_x << (to_upper_x > -bounce_buffer), (to_upper_x < 0.0); // , (population.col(3) < 0);
	bounce_ur_y << (to_upper_y > -bounce_buffer), (to_upper_y < 0.0); // , (population.col(4) < 0);

	population(select_rows(bounce_ur_x), { 3 }) = -population(select_rows(bounce_ur_x), { 3 }).abs();
	population(select_rows(bounce_ur_y), { 4 }) = -population(select_rows(bounce_ur_y), { 4 }).abs();

	population(select_rows(bounce_ur_x), { 1 }) = xbounds(select_rows(bounce_ur_x), { 1 }) - bounce_buffer;
	population(select_rows(bounce_ur_y), { 2 }) = ybounds(select_rows(bounce_ur_y), { 1 }) - bounce_buffer;

	// Attract outside individuals returning to the world
	ArrayXXb lo_outside_x(to_lower_x.rows(), 1), lo_outside_y(to_lower_y.rows(), 1);
	lo_outside_x << (to_lower_x < 0.0); // , (population.col(3) < 0);
	lo_outside_y << (to_lower_y < 0.0); // , (population.col(4) < 0);

	wall_force(select_rows(lo_outside_x), { 0 }) += (1 / to_lower_x(select_rows(lo_outside_x)).pow(1)).abs();
	wall_force(select_rows(lo_outside_y), { 1 }) += (1 / to_lower_y(select_rows(lo_outside_y)).pow(1)).abs();
	// wall_force(select_rows(lo_outside_x), { 0 }) -= (1 / to_lower_x(select_rows(lo_outside_x)).pow(1)).abs();
	// wall_force(select_rows(lo_outside_y), { 0 }) -= (1 / to_lower_x(select_rows(lo_outside_y)).pow(1)).abs();

	ArrayXXb ur_outside_x(to_upper_x.rows(), 1), ur_outside_y(to_upper_y.rows(), 1);
	ur_outside_x << (to_upper_x < 0.0); // , (population.col(3) < 0);
	ur_outside_y << (to_upper_y < 0.0); // , (population.col(4) < 0);

	wall_force(select_rows(ur_outside_x), { 0 }) += (1 / to_lower_x(select_rows(ur_outside_x)).pow(1)).abs();
	wall_force(select_rows(ur_outside_y), { 1 }) += (1 / to_lower_y(select_rows(ur_outside_y)).pow(1)).abs();
	// wall_force(select_rows(ur_outside_x), { 0 }) -= (1 / to_upper_x(select_rows(ur_outside_x)).pow(1)).abs();
	// wall_force(select_rows(ur_outside_y), { 0 }) -= (1 / to_upper_y(select_rows(ur_outside_y)).pow(1)).abs();

	// // Repelling force
	// wall_force[:, i] += np.maximum((-1 / wall_buffer * *1 + 1 / to_lower * *1), 0)
	// wall_force[:, i] -= np.maximum((-1 / wall_buffer * *1 + 1 / to_upper * *1), 0)

	// Repelling force
	// wall_force[:, i] += np.maximum((1 / to_lower), 0)
	// wall_force[:, i] -= np.maximum((1 / to_upper), 0)

	ArrayXXb inside_wall_lower_x(to_lower_x.rows(), 2), inside_wall_lower_y(to_lower_y.rows(), 2);
	inside_wall_lower_x << (to_lower_x < wall_buffer), (to_lower_x > -bounce_buffer);
	inside_wall_lower_y << (to_lower_y < wall_buffer), (to_lower_y > -bounce_buffer);

	ArrayXXb inside_wall_upper_x(to_upper_x.rows(), 2), inside_wall_upper_y(to_upper_y.rows(), 2);
	inside_wall_upper_x << (to_upper_x < wall_buffer), (to_lower_x > -bounce_buffer);
	inside_wall_upper_y << (to_upper_y < wall_buffer), (to_lower_y > -bounce_buffer);

	Eigen::ArrayXf tlx_s = to_lower_x(select_rows(inside_wall_lower_x));
	Eigen::ArrayXf tly_s = to_lower_y(select_rows(inside_wall_lower_y));
	Eigen::ArrayXf tux_s = to_upper_x(select_rows(inside_wall_upper_x));
	Eigen::ArrayXf tuy_s = to_upper_y(select_rows(inside_wall_upper_y));

	wall_force(select_rows(inside_wall_lower_x), { 0 }) += (1 / tlx_s * tlx_s);
	wall_force(select_rows(inside_wall_lower_y), { 1 }) += (1 / tly_s * tly_s);

	wall_force(select_rows(inside_wall_upper_x), { 0 }) -= (1 / tux_s * tux_s);
	wall_force(select_rows(inside_wall_upper_y), { 1 }) -= (1 / tuy_s * tuy_s);

	population(Eigen::all, { 15,16 }) += wall_force;

	// Update forces
	return population;
}

/*-----------------------------------------------------------*/
/*                   Update repulsive forces                 */
/*-----------------------------------------------------------*/
Eigen::ArrayXXf update_repulsive_forces(Eigen::ArrayXXf population, double social_distance_factor)
{
	/*calculated repulsive forces between individuals

	Function that calculates repulsion forces between individuals during social distancing.

	Keyword arguments
	---------------- -
	population : ndarray
	the array containing all the population information

	social_distance_factor : float
	Amplitude of repulsive force used to enforce social distancing
	*/

	int pop_size = population.rows();

	float epsilon = 1e-4; // to avoid division by zero errors
	Eigen::ArrayXXf dist = pairwise_dist(population(Eigen::all, { 1,2 })) + epsilon;

	Eigen::ArrayXXf dist_sqrt = dist.sqrt();
	dist += Eigen::MatrixXf::Identity(pop_size, pop_size).array();
	dist_sqrt += Eigen::MatrixXf::Identity(pop_size, pop_size).array();

	//cout.precision(20);

	//cout << dist(1092, 1570) << endl;
	//cout << dist(1570, 1092) << endl;
	//cout << population(1092, { 1,2 }) << endl;
	//cout << population(1570, { 1,2 }) << endl;

	//cout << pairwise_dist(population({ 1092,1570 }, { 1,2 }), id) << endl;

	Eigen::ArrayXXf to_point_x = pairwise_diff(population.col(1));
	Eigen::ArrayXXf to_point_y = pairwise_diff(population.col(2));

	//cout << "to point x" << endl;
	//for (int idx : population.col(0)) {

	//	if (to_point_x.row(idx).isNaN().any()) {

	//		int id_col = 0;
	//		for (float col : to_point_x.row(idx)) {

	//			if (isnan(col)) {

	//				cout << "row: " << idx << " col: " << id_col << endl;
	//				cout << population(idx, { 1,2 }) << endl;
	//				//cout << population.row(idx);
	//			}

	//			id_col++;
	//		}

	//	}
	//}

	//cout << "dist_sqrt" << endl;
	//for (int idx : population.col(0)) {

	//	if (dist_sqrt.row(idx).isNaN().any()) {

	//		int id_col = 0;
	//		for (float col : dist_sqrt.row(idx)) {

	//			if (isnan(col)) {

	//				cout << "row: " << idx << " col: " << id_col << endl;
	//				//cout << population.row(idx);
	//			}

	//			id_col++;
	//		}

	//	}
	//}

	//cout << "dist" << endl;
	//for (int idx : population.col(0)) {

	//	if (dist.row(idx).isNaN().any()) {

	//		int id_col = 0;
	//		for (float col : dist.row(idx)) {

	//			if (isnan(col)) {

	//				cout << "row: " << idx << " col: " << id_col << endl;
	//				//cout << population.row(idx);
	//			}

	//			id_col++;
	//		}

	//	}
	//}

	//Eigen::ArrayXf repulsion_force_x = -social_distance_factor * (to_point_x / dist.pow(2.5)).rowwise().sum();
	//Eigen::ArrayXf repulsion_force_y = -social_distance_factor * (to_point_y / dist.pow(2.5)).rowwise().sum();

	Eigen::ArrayXf repulsion_force_x = -social_distance_factor * (to_point_x / (dist * dist * dist_sqrt)).rowwise().sum();
	Eigen::ArrayXf repulsion_force_y = -social_distance_factor * (to_point_y / (dist * dist * dist_sqrt)).rowwise().sum();

	//id = 0;
	//for (float force : repulsion_force_x) {

	//	if ((isinf(force)) || (isnan(force))) {
	//		repulsion_force_x(id) = 0.0;
	//		repulsion_force_y(id) = 0.0;
	//		cout << "row: " << id << endl;
	//		//cout << "to_point" << endl;
	//		//cout << to_point_x.row(id) << endl;
	//		//cout << to_point_y.row(id) << endl;
	//		//cout << "dist" << endl;
	//		//cout << dist.row(id) << endl;
	//		//cout << "dist_sqrt" << endl;
	//		//cout << dist_sqrt.row(id) << endl;
	//		//cout << "population" << endl;
	//		//cout << population.col(1).transpose() << endl;
	//		//cout << population.col(2).transpose() << endl;
	//	}
	//	id++;
	//}

	population.col(15) += repulsion_force_x;
	population.col(16) += repulsion_force_y;

	// Update forces
	return population;
}

/*-----------------------------------------------------------*/
/*                    Update gravity forces                  */
/*-----------------------------------------------------------*/
tuple<Eigen::ArrayXXf, double> update_gravity_forces(Eigen::ArrayXXf population, double time, double last_step_change, RandomDevice *my_rand, double wander_step_size,
	double gravity_strength, double wander_step_duration)
{
	/*updates random perturbation in forces near individuals to cause random motion

	Function that returns geometric parameters of the destination
	that the population members have set.

	Keyword arguments :
	------------------
	population : ndarray
	the array containing all the population information

	time : float
	current simulation time

	last_step_change : float
	last time value at which a random perturbation was introduced

	wander_step_size, gravity_strength, wander_step_duration : float
	proximity of perturbation to individuals,
	strength of attracion to perturbation,
	length of time perturbation is present
	*/

	int pop_size = population.rows();

	// Gravity
	if (wander_step_size != 0.0) {
		if ((time - last_step_change) > wander_step_duration)
		{
			Eigen::ArrayXXf vect_un = my_rand->uniform_dist(-1, 1, pop_size, 2);
			Eigen::ArrayXXf vect = vect_un.colwise() / vect_un.rowwise().norm().array();

			Eigen::ArrayXXf gravity_well = population(Eigen::all, { 1,2 }) + wander_step_size * vect;
			last_step_change = time;

			Eigen::ArrayXXf to_well = (gravity_well - population(Eigen::all, { 1,2 }));
			Eigen::ArrayXf dist = to_well.rowwise().norm().array();

			population(select_rows(dist != 0), { 15 }) += gravity_strength * to_well(select_rows(dist != 0), { 0 }) / (dist(select_rows(dist != 0)).pow(3));
			population(select_rows(dist != 0), { 16 }) += gravity_strength * to_well(select_rows(dist != 0), { 1 }) / (dist(select_rows(dist != 0)).pow(3));
		}

	}


	return {population, last_step_change};
}

/*-----------------------------------------------------------*/
/*                  Get motion parameters                    */
/*-----------------------------------------------------------*/
vector<double> get_motion_parameters(double xmin, double ymin, double xmax, double ymax)
{

	/*gets destination center and wander ranges

	Function that returns geometric parameters of the destination
	that the population members have set.

	Keyword arguments :
------------------
	xmin, ymin, xmax, ymax : int or float
	lower and upper bounds of the destination area set.
	*/

	double x_center = xmin + ((xmax - xmin) / 2);
	double y_center = ymin + ((ymax - ymin) / 2);

	double x_wander = (xmax - xmin) / 2;
	double y_wander = (ymax - ymin) / 2;

	return { x_center, y_center, x_wander, y_wander };
}