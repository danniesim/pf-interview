import React from 'react';
import PropTypes from 'prop-types';
import {
	MultiDropdownList,
	MultiList,
	SingleDropdownRange,
	RangeSlider,
    DataSearch,
} from '@appbaseio/reactivesearch';


const SearchFilters = ({ visible }) => (
    <div className={`flex column filters-container ${!visible ? 'hidden' : ''}`}>
		<div className="child m10">
			<MultiList
				componentId="industry_a"
				dataField="INDUSTRY_MAP_A.raw"
				placeholder="Enter or Select Industry"
				title="Division A: Agriculture, Forestry, And Fishing"
				filterLabel="Div A"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
        <div className="child m10">
			<MultiList
				componentId="industry_b"
				dataField="INDUSTRY_MAP_B.raw"
				placeholder="Enter or Select Industry"
				title="Division B: Mining"
				filterLabel="Div B"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
        <div className="child m10">
			<MultiList
				componentId="industry_c"
				dataField="INDUSTRY_MAP_C.raw"
				placeholder="Enter or Select Industry"
				title="Division C: Construction"
				filterLabel="Div C"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
        <div className="child m10">
			<MultiList
				componentId="industry_d"
				dataField="INDUSTRY_MAP_D.raw"
				placeholder="Enter or Select Industry"
				title="Division D: Manufacturing"
				filterLabel="Div D"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
        <div className="child m10">
			<MultiList
				componentId="industry_e"
				dataField="INDUSTRY_MAP_E.raw"
				placeholder="Enter or Select Industry"
				title="Division E: Transportation, Communications, Electric, Gas, And Sanitary Services"
				filterLabel="Div E"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
        <div className="child m10">
			<MultiList
				componentId="industry_f"
				dataField="INDUSTRY_MAP_F.raw"
				placeholder="Enter or Select Industry"
				title="Division F: Wholesale Trade"
				filterLabel="Div F"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
        <div className="child m10">
			<MultiList
				componentId="industry_g"
				dataField="INDUSTRY_MAP_G.raw"
				placeholder="Enter or Select Industry"
				title="Division G: Retail Trade"
				filterLabel="Div G"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
        <div className="child m10">
			<MultiList
				componentId="industry_h"
				dataField="INDUSTRY_MAP_H.raw"
				placeholder="Enter or Select Industry"
				title="Division H: Finance, Insurance, And Real Estate"
				filterLabel="Div H"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
        <div className="child m10">
			<MultiList
				componentId="industry_i"
				dataField="INDUSTRY_MAP_I.raw"
				placeholder="Enter or Select Industry"
				title="Division I: Services"
				filterLabel="Div I"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
        <div className="child m10">
			<MultiList
				componentId="industry_j"
				dataField="INDUSTRY_MAP_J.raw"
				placeholder="Enter or Select Industry"
				title="Division J: Public Administration"
				filterLabel="Div J"
				size={1000}
				sortBy="asc"
				queryFormat="or"
				showCount="false"
			/>
		</div>
		<div className="child m10">
			<MultiList
				componentId="geography"
				dataField="GEOGRAPHY.raw"
				placeholder="Enter or Select Geography"
				title="Geography"
				filterLabel="Geography"
				size={1000}
				queryFormat="or"
			/>
		</div>
    </div>
);

SearchFilters.propTypes = {
	visible: PropTypes.bool,
};

export default SearchFilters;