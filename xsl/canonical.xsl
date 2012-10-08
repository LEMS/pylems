<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="xml" omit-xml-declaration="no" indent="yes" version="1.0"/>
  
  <xsl:preserve-space elements="*"/>
 
 
 	<xsl:template match="Lems">
 		<Lems>
 			<xsl:apply-templates/>
 		</Lems>
 	</xsl:template>
 
 
 	<xsl:template match="Target|Unit|Dimension|ComponentType|Component|Assertion|Include">
 		<xsl:copy-of select="."/>
 	</xsl:template>
 
 
 
 	<xsl:template match="*">
 		<Component>
 			<xsl:attribute name="type"><xsl:value-of select="local-name()"/></xsl:attribute>
 			<xsl:copy-of select="@*"/>
	 		<xsl:apply-templates mode="incomponent"/>
 		</Component>
 	</xsl:template>
 
 
 	<xsl:template match="*" mode="incomponent">
 		<Component>
 			<xsl:choose>
 				<xsl:when test="@type">
 					<xsl:attribute name="child"><xsl:value-of select="local-name()"/></xsl:attribute>	
 				</xsl:when>
				<xsl:otherwise>
		 			<xsl:attribute name="type"><xsl:value-of select="local-name()"/></xsl:attribute>		
				</xsl:otherwise>
 			</xsl:choose>
 
 			<xsl:copy-of select="@*"/>
	 		<xsl:apply-templates mode="incomponent"/>
 		</Component>
 	</xsl:template>
 
 
 </xsl:stylesheet>
